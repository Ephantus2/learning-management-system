from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Assessment, Submission, Grade, Performance
from django.shortcuts import get_object_or_404
from users.permissions import IsStudent, IsLecturer, IsAdmin, IsLecturerOrAdmin
from .serializers import AssessmentSerializer, SubmissionSerializer, GradeSerializer, StudentPerformanceSerializer
from .services import calculate_student_performance
from academics.models import AcademicYear
from courses.models import Enrollment
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()
class AssessmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request):
        academic_year = get_object_or_404(AcademicYear, is_current=True)
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():

            course = serializer.validated_data["course"]

            lecturer_profile = getattr(
                request.user,
                "lecturer_profile",
                None
            )

            if(
                lecturer_profile is None
                or course.lecturer_id != lecturer_profile.id
            ):
                return Response(
                    {
                        "error": "You are not assigned to this course."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            assessment = serializer.save(lecturer=request.user, academic_year=academic_year)
            return Response(AssessmentSerializer(assessment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateDeleteAssessmentView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def put(self, request, pk):
        assessment = get_object_or_404(Assessment, pk=pk)
        serializer = AssessmentSerializer(assessment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        assessment = get_object_or_404(Assessment, pk=pk)
        assessment.delete()
        return Response({"message": "Assessment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class courseAssessmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_code):
        assessments = Assessment.objects.filter(course__code=course_code)
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmissionCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        assessment_id = request.data.get("assessment")
        assessment = get_object_or_404(Assessment, pk=request.data.get('assessment'))
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=assessment.course
        ).exists()

        if not is_enrolled:
            return Response(
                {
                    "error": "you are not enrolled in this course"
                },
                status = status.HTTP_403_FORBIDDEN
            )

        if assessment.assessment_mode != "ONLINE":
            return Response(
                {
                    "error": "This assessment does not accept online submission"
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = SubmissionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(student=request.user, assessment=assessment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateDeleteSubmissionView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def put(self, request, pk):
        submission = get_object_or_404(Submission, pk=pk)
        serializer = SubmissionSerializer(submission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        submission = get_object_or_404(Submission, pk=pk)
        submission.delete()
        return Response({"message": "Submission deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class submissionsView(APIView):
    permission_classes = [IsLecturerOrAdmin]

    def get(self, request, pk):
        submissions = Submission.objects.filter(assessment = Assessment.objects.get(pk=pk))
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MySubmissionsView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        submissions = Submission.objects.filter(student=request.user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GradeCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsLecturer
    ]

    def post(self, request):

        serializer = GradeSerializer(
            data=request.data
        )

        if serializer.is_valid():

            grade = serializer.save(graded_by=request.user)

            calculate_student_performance(
                student=grade.student,
                course=grade.assessment.course,
                academic_year=grade.assessment.academic_year
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class GradeUpdateView(APIView):

    permission_classes = [
        IsLecturer
    ]

    def put(self, request, pk):

        grade = get_object_or_404(
            Grade.objects.select_related(
               "assessment",
               "assessment__course",
               "assessment__academic_year",
               "student"
            ),
            pk=pk
        )

        lecturer_profile = getattr(
            request.user,
            "lecturer_profile",
            None
        )

        if(
            lecturer_profile is None
            or grade.assessment.course.lecturer_id != lecturer_profile.id
        ):
            return Response(
                {
                    "error": "You are not authorized to update this grade"
                },
                status = status.HTTP_403_FORBIDDEN
            )
        
        serializer = GradeSerializer(
            grade,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():

            grade = serializer.save(
                graded_by = request.user
            )

            performance = calculate_student_performance(
                student=grade.student,
                course=grade.assessment.course,
                academic_year=grade.assessment.course.academic_year
            )

            return Response(
                {
                    "message": "Grade updated successfully.",
                    "grade": GradeSerializer(grade).data,
                    "performance": {
                        "total_marks": performance.total_marks,
                        "grade": performance.grade
                    }
                },
                status=status.HTTP_200_OK
            )


from decimal import Decimal, InvalidOperation
class BulkGradeCreateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsLecturer
    ]

    def post(self, request, assessment_id):

        # 1. Get the assessment.
        assessment = get_object_or_404(
            Assessment.objects.select_related(
                "course",
                "academic_year"
            ),
            pk=assessment_id
        )

        # 2. Verify that the lecturer is assigned to this course.
        lecturer_profile = getattr(
            request.user,
            "lecturer_profile",
            None
        )

        if (
            lecturer_profile is None
            or assessment.course.lecturer_id != lecturer_profile.id
        ):
            return Response(
                {
                    "error": "You are not authorized to grade this assessment."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Get the submitted marks.
        marks_data = request.data.get("marks")

        if not isinstance(marks_data, list) or not marks_data:
            return Response(
                {
                    "error": "Provide a non-empty list of student marks."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_marks = []
        seen_registration_numbers = set()
        errors = []

        # 4. Validate every entry.
        for index, row in enumerate(marks_data):

            if not isinstance(row, dict):
                errors.append({
                    "row": index + 1,
                    "error": "Each entry must be an object."
                })
                continue

            registration_number = row.get(
                "registration_number"
            )

            raw_marks = row.get("marks")

            if not registration_number or raw_marks is None:
                errors.append({
                    "row": index + 1,
                    "error": (
                        "Registration number and marks are required."
                    )
                })
                continue

            registration_number = registration_number.strip()

            # Prevent duplicate entries in the same request.
            if registration_number in seen_registration_numbers:
                errors.append({
                    "row": index + 1,
                    "registration_number": registration_number,
                    "error": "Duplicate registration number."
                })
                continue

            seen_registration_numbers.add(
                registration_number
            )

            # Find the student using the registration number.
            student = User.objects.filter(
                login_id=registration_number,
                role=User.Role.STUDENT
            ).first()

            if student is None:
                errors.append({
                    "row": index + 1,
                    "registration_number": registration_number,
                    "error": "Student not found."
                })
                continue

            # Confirm that the student is enrolled in this course.
            enrolled = Enrollment.objects.filter(
                student=student,
                course=assessment.course
            ).exists()

            if not enrolled:
                errors.append({
                    "row": index + 1,
                    "registration_number": registration_number,
                    "error": "Student is not enrolled in this course."
                })
                continue

            # Validate marks using Decimal.
            try:
                marks = Decimal(str(raw_marks))
            except (ValueError, TypeError, InvalidOperation):
                errors.append({
                    "row": index + 1,
                    "registration_number": registration_number,
                    "error": "Marks must be a valid number."
                })
                continue

            if not marks.is_finite():
                errors.append({
                    "row": index + 1,
                    "registration_number": registration_number,
                    "error": "Marks must be a finite number."
                })
                continue

            if marks < 0 or marks > assessment.total_marks:
                errors.append({
                    "row": index + 1,
                    "registration_number": registration_number,
                    "error": (
                        f"Marks must be between 0 and "
                        f"{assessment.total_marks}."
                    )
                })
                continue

            validated_marks.append({
                "student": student,
                "marks": marks
            })

        # 5. Reject the entire request if any row is invalid.
        # This prevents accidentally saving only part of a marksheet.
        if errors:
            return Response(
                {
                    "error": "Some marks could not be validated.",
                    "details": errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 6. Save all grades and recalculate performance.
        with transaction.atomic():

            for row in validated_marks:

                Grade.objects.update_or_create(
                    assessment=assessment,
                    student=row["student"],
                    defaults={
                        "marks": row["marks"],
                        "graded_by": request.user
                    }
                )

            # Recalculate each affected student's course result.
            for row in validated_marks:

                calculate_student_performance(
                    student=row["student"],
                    course=assessment.course,
                    academic_year=assessment.academic_year
                )

        return Response(
            {
                "message": "Marks saved successfully.",
                "assessment": assessment.title,
                "students_processed": len(validated_marks)
            },
            status=status.HTTP_200_OK
        )
    
class ViewGradeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_id, student_id):
        grade = get_object_or_404(Grade.objects.select_related(
            "student",
            "assessment",
            "assessment__course",
            "assessment__academic_year"
        ), 
        assessment_id=assessment_id,
        student_id=student_id
        )

        serializer = GradeSerializer(grade)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PerformanceView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    def get(self, request):

        academic_year = request.query_params.get(
            "academic_year"
        )

        if not academic_year:
            return Response(
                {
                    "error": "academic_year is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        academic_year = get_object_or_404(AcademicYear, name=academic_year)

        performances = Performance.objects.filter(
            student=request.user,
            academic_year=academic_year
        ).select_related(
            "course",
            "academic_year"
        ).order_by(
            "course__code"
        )

        serializer = StudentPerformanceSerializer(
            performances,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )