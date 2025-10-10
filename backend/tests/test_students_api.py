
    from rest_framework import status

    def test_unauthenticated_401(api_client):
        resp = api_client.get("/api/students/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in resp.json()

    def test_admin_full_crud(api_client, admin_user):
        api_client.force_authenticate(admin_user)
        payload = {"reg_no": "STU-1001", "name": "Alice", "program": "BBA", "status": "active"}
        resp = api_client.post("/api/students/", payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        sid = resp.json()["id"]

        resp = api_client.get("/api/students/")
        assert resp.status_code == status.HTTP_200_OK
        assert any(x["reg_no"] == "STU-1001" for x in resp.json()["results"])

        resp = api_client.get(f"/api/students/{sid}/")
        assert resp.status_code == status.HTTP_200_OK

        resp = api_client.patch(f"/api/students/{sid}/", {"status": "inactive"}, format="json")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["status"] == "inactive"

        resp = api_client.delete(f"/api/students/{sid}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
    
