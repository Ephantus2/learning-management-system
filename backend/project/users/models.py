from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, login_id, password=None, **extra_fields):

        if not login_id:
            raise ValueError("The login_id must be provided")

        user = self.model(
            login_id=login_id,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login_id, password=None, **extra_fields):
        
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            login_id,
            password,
            **extra_fields
        )


class User(AbstractUser):
    
    username = None
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        LECTURER = "LECTURER", "Lecturer"
        ADMIN = "ADMIN", "Admin"
        
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )
    
    login_id = models.CharField(max_length=100, unique=True)
    
    USERNAME_FIELD = "login_id"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    objects = UserManager()