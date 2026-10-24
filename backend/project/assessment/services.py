from decimal import Decimal

from .models import Grade, Performance


def calculate_student_performance(student, course, academic_year):

    # Get all grades belonging to this student,
    # for this course and academic year.
    grades = Grade.objects.filter(
        student=student,
        assessment__course=course,
        assessment__academic_year=academic_year
    ).select_related("assessment")

    cat_scores = []
    exam_scores = []

    for grade in grades:
        assessment = grade.assessment
        maximum_marks = Decimal(assessment.total_marks)

    marks_obtained = Decimal(grade.marks)

    if assessment.assessment_type == "CAT":
        converted_score = (
            marks_obtained / maximum_marks
        ) * Decimal("30")

        cat_scores.append(converted_score)

    elif assessment.assessment_type == "EXAM":
        converted_score = (
            marks_obtained / maximum_marks
        ) * Decimal("70")

        exam_scores.append(converted_score)

    if cat_scores:
        cat_contribution = sum(
            cat_scores, Decimal("0.00")
        ) / Decimal(len(cat_scores))

    else:
        cat_contribution = Decimal("0.00")

    if exam_scores:
        exam_contribution = sum(
            exam_scores, Decimal("0.00")
        )/ Decimal(len(exam_scores))

    else:
        exam_contribution = Decimal("0.00")


    # Calculate the sum of all marks obtained.
    total_marks = cat_contribution + exam_contribution

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