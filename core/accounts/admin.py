from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


# Register your models here.
class CustomUserAdmin(UserAdmin):
    models = User
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_active",
        "is_verified",
    )
    list_filter = (
        "email",
        "is_superuser",
        "is_active",
        "is_verified",
    )
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": (
                "is_staff", "is_active", "is_superuser", "is_verified")},
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions", "type")}),
        ("Important Date", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )

class CustomProfileAdmin(admin.ModelAdmin):
    models = Profile
    list_display = (
        "pk",
        "user",
        "first_name",
        "last_name",
        "phone_number",
    )
    search_fields = (
        "user",
        "first_name",
        "last_name",
        "phone_number",
    )

admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)
