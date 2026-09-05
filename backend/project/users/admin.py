from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LecturerProfile, StudentProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "login_id",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "login_id",
        "first_name",
        "last_name",
        "email",
    )

    ordering = ("login_id",)

    fieldsets = (
        (None, {
            "fields": (
                "login_id",
                "password",
            )
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "email",
            )
        }),

        ("RBAC", {
            "fields": (
                "role",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "login_id",
                "first_name",
                "last_name",
                "email",
                "password1",
                "password2",
                "role",
                "is_staff",
                "is_active",
            ),
        }),
    )
    
admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)