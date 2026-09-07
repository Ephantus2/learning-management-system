from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Assessment, Submission, Grade
from django.shortcuts import get_object_or_404
from users.permissions import IsStudent, IsLecturer, IsAdmin, IsLecturerOrAdmin
from .serializers import AssessmentSerializer, SubmissionSerializer, GradeSerializer

class AssessmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lecturer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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