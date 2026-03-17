from django.contrib import admin
from .models import ContactModel, NewsLetter

@admin.register(ContactModel)
class CustomContactAdmin(admin.ModelAdmin):
    models = ContactModel
    list_display = (
        "id",
        "subject",
        "is_checked",
        "created_date",
    )

@admin.register(NewsLetter)
class CustomContactAdmin(admin.ModelAdmin):
    models = NewsLetter
    list_display = (
        "id",
        "email",
        "created_date",
    )