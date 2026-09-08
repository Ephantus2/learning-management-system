from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Enrollment, Course, CourseMaterial
from django.db import IntegrityError
from users.permissions import IsStudent, IsLecturer, IsAdmin, IsLecturerOrAdmin
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser  


from .serializers import CourseMaterialSerializer, CourseSerializer



class CourseCreateView(APIView):

    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):

    permission_classes = [IsAdmin]

    def put(self, request, pk):

        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class SearchCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        courses = Course.objects.filter(code__icontains=query)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseMaterialCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
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
class UpdateDeleteCourseMaterialView(APIView):
    permission_classes = [IsAuthenticated, IsLecturerOrAdmin]

    def put(self, request, pk):
        material = get_object_or_404(CourseMaterial, pk=pk)
        serializer = CourseMaterialSerializer(
            material,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        material = get_object_or_404(CourseMaterial, pk=pk)
        material.delete()
        return Response({"message": "Course material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class viewCourseMaterialsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_code):
        materials = CourseMaterial.objects.filter(course__code=course_code)
        serializer = CourseMaterialSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

class EnrolledUnits(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        student = request.user
        enrollments = Enrollment.objects.filter(student=student)
        courses = [enrollment.course for enrollment in enrollments]
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EnrolmentStatisticsView(APIView):
    permission_classes = [IsLecturerOrAdmin]

    def get(self, request, course_code):
        course = get_object_or_404(Course, code=course_code)
        total_enrollments = Enrollment.objects.filter(course=course).count()
        return Response({"course": course.name, "total_enrollments": total_enrollments}, status=status.HTTP_200_OK)