from django.db.models import Sum

from .models import Grade, Performance


def calculate_student_performance(
    student,
    course,
    academic_year
):

    grades = Grade.objects.filter(
        submission__student=student,
        submission__assessment__course=course,
        submission__assessment__academic_year=academic_year
    )

    total_marks = grades.aggregate(
        total=Sum("marks")
    )["total"] or 0

    if total_marks >= 70:
        grade = "A"

    elif total_marks >= 60:
        grade = "B"

    elif total_marks >= 50:
        grade = "C"

    elif total_marks >= 40:
        grade = "D"

    else:
        grade = "F"

    performance, created = Performance.objects.update_or_create(
        student=student,
        course=course,
        academic_year=academic_year,

        defaults={
            "total_marks": total_marks,
            "grade": grade
        }
    )

    return performance