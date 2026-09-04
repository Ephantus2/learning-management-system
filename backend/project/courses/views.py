from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import IsLecturerOrAdmin


class CourseCreateView(APIView):

    permission_classes = [IsLecturerOrAdmin]

    def post(self, request):

        return Response({
            "message": "Course created"
        })

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CourseMaterial
from .serializers import CourseMaterialSerializer
from users.permissions import IsLecturer


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