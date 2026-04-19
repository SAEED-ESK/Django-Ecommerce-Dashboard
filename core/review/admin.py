from django.contrib import admin
from .models import ReviewModel

@admin.register(ReviewModel)
class CustomReviewAdmin(admin.ModelAdmin):
    models = ReviewModel
    list_display = (
        "id",
        "user",
        "product",
        "rate",
        "created_date",
    )
