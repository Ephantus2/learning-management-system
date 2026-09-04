from django.contrib import admin
from .models import Course, Enrollment, CourseMaterial
# Register your models here.

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(CourseMaterial)