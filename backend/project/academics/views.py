from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import SchoolSerializer, ProgrammeSerializer, DepartmentSerializer, AcademicYearSerializer
from .models import School, Programme, Department, AcademicYear
from users.permissions import IsStudent
from users.models import StudentProfile
from django.shortcuts import get_object_or_404

from django.core.cache import cache

class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProgrammeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = cache.get("programmes")
        if data is None:
            programmes = Programme.objects.all()
            serializer = ProgrammeSerializer(programmes, many=True)
            data = serializer.data
            cache.set("programmes", data, timeout=300)
        return Response(data, status=status.HTTP_200_OK)

class AcademicYearView(APIView):
    permission_classes = [IsStudent]
    
    def get(self, request):
        user = request.user
        admission_year = get_object_or_404(StudentProfile, user_id=user.id).admission_year
        
        academic_years = AcademicYear.objects.filter(start_year__gte=admission_year)
        serializers = AcademicYearSerializer(academic_years, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    