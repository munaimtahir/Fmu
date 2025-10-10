
    from rest_framework import status
    from sims_backend.admissions.models import Student

    def test_student_can_read_own_only(api_client, student_user):
        me = Student.objects.create(reg_no=student_user.username, name="Me", program="Prog", status="active")
        other = Student.objects.create(reg_no="STU-9999", name="Other", program="X", status="inactive")

        api_client.force_authenticate(student_user)

        resp = api_client.get("/api/students/")
        assert resp.status_code == status.HTTP_200_OK
        results = resp.json()["results"]
        assert len(results) == 1 and results[0]["reg_no"] == student_user.username

        resp = api_client.get(f"/api/students/{me.id}/")
        assert resp.status_code == status.HTTP_200_OK

        resp = api_client.get(f"/api/students/{other.id}/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_student_cannot_create_update_delete(api_client, student_user):
        api_client.force_authenticate(student_user)
        resp = api_client.post("/api/students/", {"reg_no": "STU-7777","name":"New","program":"P","status":"active"}, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN
    
