from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Programme(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="programmes"
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class AcademicYear(models.Model):

    name = models.CharField(
        max_length=9,
        unique=True
    )

    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name