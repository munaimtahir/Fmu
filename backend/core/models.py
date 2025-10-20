from __future__ import annotations

from django.db import models


class TimeStampedModel(models.Model):
    """Reusable base model that tracks creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def touch(self, using: str | None = None, update_fields: set[str] | None = None) -> None:
        """Force an update to refresh the ``updated_at`` timestamp."""
        # Call save with appropriate arguments to update the timestamp
        if update_fields is not None:
            self.save(using=using, update_fields=update_fields)
        else:
            self.save(using=using)
