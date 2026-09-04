# serializers.py

from rest_framework import serializers
from .models import CourseMaterial


class CourseMaterialSerializer(serializers.ModelSerializer):

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