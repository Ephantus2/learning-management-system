from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import IsLecturerOrAdmin


class CourseCreateView(APIView):

    permission_classes = [IsLecturerOrAdmin]

    def post(self, request):

        return Response({
            "message": "Course created"
        })
