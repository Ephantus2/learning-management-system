from rest_framework import serializers
from .models import Assessment, Submission, Grade

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id",
            "course",
            "lecturer",
            "title",
            "description",
            "assessment_type",
            "total_marks",
            "due_date",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "lecturer",
            "created_at"
        ]

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "id",
            "assessment",
            "student",
            "answer",
            "file",
            "submitted_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "student",
            "submitted_at",
            "updated_at"
        ]

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = [
            "id",
            "submission",
            "marks",
            "feedback",
            "graded_at"
        ]
        read_only_fields = [
            "id",
            "graded_at"
        ]