# serializers.py

from rest_framework import serializers
from .models import CourseMaterial, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "name", "description", "lecturer", "programme", "created_at" ]

    def validate_code(self, value):
        if Course.objects.filter(code=value).exists():
            raise serializers.ValidationError("Course with this code already exists.")
        return value

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        return course

class CourseMaterialSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field="code",
        queryset=Course.objects.all()
    )
    class Meta:
        model = CourseMaterial
        fields = [
            "id",
            "course",
            "lecturer",
            "title",
            "file",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "lecturer",
            "uploaded_at",
        ]