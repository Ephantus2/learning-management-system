from decimal import Decimal

from .models import Grade, Performance


def calculate_student_performance(student, course, academic_year):

    # Get all grades belonging to this student,
    # for this course and academic year.
    grades = Grade.objects.filter(
        student=student,
        assessment__course=course,
        assessment__academic_year=academic_year
    )

    # Calculate the sum of all marks obtained.
    total_marks = sum(
        (grade.marks for grade in grades),
        Decimal("0.00")
    )

    # Determine the student's letter grade.
    # IMPORTANT: Replace these example thresholds with
    # your university's official grading policy.
    if total_marks >= 70:
        letter_grade = "A"
    elif total_marks >= 60:
        letter_grade = "B"
    elif total_marks >= 50:
        letter_grade = "C"
    elif total_marks >= 40:
        letter_grade = "D"
    else:
        letter_grade = "F"

    # Create or update the student's performance record.
    performance, created = Performance.objects.update_or_create(
        student=student,
        course=course,
        academic_year=academic_year,
        defaults={
            "total_marks": total_marks,
            "grade": letter_grade
        }
    )

    return performance