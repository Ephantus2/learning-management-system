from django.db import models
from courses.models import Course
from django.conf import settings
from academics.models import AcademicYear

# Create your models here.
class Assessment(models.Model):
    class AssessmentType(models.TextChoices):
        CAT = "CAT", "CAT"
        ASSIGNMENT = "ASSIGNMENT", "Assignment"
        EXAM = "EXAM", "Exam"

    course = models.ForeignKey(
        Course,
        on_delete = models.CASCADE,
        related_name="assessments"
    )

    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_assassments"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assessment_type = models.CharField(
        max_length=20,
        choices = AssessmentType.choices
    )

    total_marks = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

class Submission(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "submissions"
    )

    answer = models.TextField(blank=True)
    file = models.FileField(upload_to="submissions/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.login_id} - {self.assessment.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["assessment", "student"],
                name = "unique_student_assessment_submission"
            )
        ]

class Grade(models.Model):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name="grade"
    ) 
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)

    graded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.submission.student.login_id} - {self.submission.assessment.title} - {self.marks}"



class Performance(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="performances"
    )

    total_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    class Grade(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"
        F = "F", "F"
        I = "I", "Incomplete"

    grade = models.CharField(
        max_length=1,
        choices=Grade.choices,
        default=Grade.I
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "course",
                    "academic_year"
                ],
                name="unique_student_course_academic_year"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.login_id} - "
            f"{self.course.code} - "
            f"{self.academic_year.name}"
        )