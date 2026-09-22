from rest_framework import serializers
from .models import Programme, Department, School

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'school', 'name', 'code']

class ProgrammeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Programme
        fields = ['id', 'department', 'name', 'code']

