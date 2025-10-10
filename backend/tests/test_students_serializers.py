
    from sims_backend.admissions.serializers import StudentSerializer

    def test_student_serializer_valid():
        data = {"reg_no": "STU-100", "name": "Jane Doe", "program": "BSc CS", "status": "active"}
        s = StudentSerializer(data=data)
        assert s.is_valid(), s.errors
        obj = s.save()
        assert obj.id is not None
        assert obj.reg_no == "STU-100"

    def test_student_serializer_invalid():
        s = StudentSerializer(data={"name": "x", "program": "y", "status": "z"})
        assert not s.is_valid()
        assert "reg_no" in s.errors
    
