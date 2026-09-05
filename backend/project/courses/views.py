from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import IsLecturerOrAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CourseMaterial
from .serializers import CourseMaterialSerializer
from users.permissions import IsLecturer


class CourseCreateView(APIView):

    permission_classes = [IsLecturerOrAdmin]

    def post(self, request):

        return Response({
            "message": "Course created"
        })

# views.py


class CourseMaterialCreateView(APIView):

    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request):

        serializer = CourseMaterialSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                lecturer=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Enrollment
from django.db import IntegrityError
from users.permissions import IsStudent
from .models import Course
from django.shortcuts import get_object_or_404


class EnrollCourseView(APIView):
    permission_classes=[IsStudent]
    
    def post(self, request):
        student = request.user
        course_code = request.data.get('course_code')
        
        course = get_object_or_404(Course, code=course_code)
        
        try:
            Enrollment.objects.create(student=student, course=course)
            return Response({"message": f"{course} enrolled successfully"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"Error": "you are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
        
class UnenrollCourseView(APIView):
    permission_classes=[IsStudent]
    
    def post(self, request):
        student = request.user
        course_code = request.data.get('course_code')
        
        course = get_object_or_404(Course, code=course_code)
        
        enrollment = get_object_or_404(Enrollment, student=student, course=course)
        
        enrollment.delete()
        return Response({"message": f"{course_code} unenrolled"})