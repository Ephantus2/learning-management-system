from django.contrib import admin

# Register your models here.
from .models import School, Department, Programme, AcademicYear

admin.site.register(School)
admin.site.register(Department)
admin.site.register(Programme)
admin.site.register(AcademicYear)