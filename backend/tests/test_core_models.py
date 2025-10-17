import time

import pytest
from django.utils import timezone

from sims_backend.admissions.models import Student


@pytest.mark.django_db
class TestTimeStampedModel:
    def test_student_has_timestamp_fields(self):
        student = Student.objects.create(
            reg_no="REG-001",
            name="Test Student",
            program="BSc Computer Science",
            status="active",
        )

        assert student.created_at is not None
        assert student.updated_at is not None
        assert student.created_at <= timezone.now()
        assert student.updated_at <= timezone.now()

    def test_updated_at_changes_on_save(self):
        student = Student.objects.create(
            reg_no="REG-002",
            name="Another Student",
            program="BSc Information Technology",
            status="active",
        )

        original_updated = student.updated_at
        time.sleep(0.1)
        student.status = "inactive"
        student.save()
        student.refresh_from_db()

        assert student.updated_at > original_updated

        second_checkpoint = student.updated_at
        time.sleep(0.1)
        student.touch()
        student.refresh_from_db()

        assert student.updated_at > second_checkpoint
