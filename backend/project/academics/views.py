from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import SchoolSerializer, ProgrammeSerializer, DepartmentSerializer
from .models import School, Programme, Department

class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProgrammeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        programmes = Programme.objects.all()
        serializer = ProgrammeSerializer(programmes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)