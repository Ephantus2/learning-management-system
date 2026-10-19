from rest_framework import serializers
from .models import Assessment, Submission, Grade
from courses.serializers import UserSerializer, CourseSerializer
from .models import Performance
class AssessmentSerializer(serializers.ModelSerializer):

    lecturer = UserSerializer(read_only=True)
    #course = CourseSerializer(read_only=True)
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
            "created_at",
            "academic_year",
            "assessment_mode"
        ]
        read_only_fields = [
            "id",
            "lecturer",
            "created_at",
            "academic_year"
        ]

class SubmissionSerializer(serializers.ModelSerializer):
    assessment = AssessmentSerializer(read_only=True)
    student = UserSerializer(read_only=True)
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
            "assessment",
            "student",
            "marks",
            "feedback",
            "graded_by",
            "graded_at"
        ]
        read_only_fields = [
            "id",
            "graded_by",
            "graded_at"
        ]

    def validate(self, attrs):
        assessment = attrs.get(
            "assessment",
            getattr(self.instance, "assessment", None)
        )

        marks = attrs.get(
            "marks",
            getattr(self.instance, "marks", None)
        )

        if assessment is not None and marks is not None:
            if marks < 0:
                raise serializers.ValidationError(
                    {
                        "marks": "Marks cannot be negative"
                    }
                )
            if marks > assessment.total_marks:
                raise serializers.ValidationError(
                    {
                        "marks": (
                            f"Marks cannot exceed"
                            f"{assessment.total_marks}."
                        )
                    }
                )
        return attrs

class StudentPerformanceSerializer(
    serializers.ModelSerializer
):

    course_code = serializers.CharField(
        source="course.code",
        read_only=True
    )

    course_name = serializers.CharField(
        source="course.name",
        read_only=True
    )

    academic_year = serializers.CharField(
        source="academic_year.name",
        read_only=True
    )

    class Meta:

        model = Performance

        fields = [
            "id",
            "course_code",
            "course_name",
            "academic_year",
            "total_marks",
            "grade",
        ]