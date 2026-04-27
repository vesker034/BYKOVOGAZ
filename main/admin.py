from django.contrib import admin

from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "title_en", "employment_type", "is_active", "display_order")
    list_display_links = ("title",)
    list_filter = ("is_active", "employment_type")
    search_fields = (
        "title",
        "title_en",
        "department",
        "department_en",
        "location",
        "location_en",
        "summary",
        "summary_en",
        "requirements",
        "requirements_en",
    )
    list_editable = ("is_active", "display_order")
    ordering = ("display_order", "-created_at")
    fieldsets = (
        ("Русский", {
            "fields": ("title", "department", "location", "summary", "requirements"),
        }),
        ("English", {
            "fields": ("title_en", "department_en", "location_en", "summary_en", "requirements_en"),
        }),
        ("Параметры публикации", {
            "fields": ("employment_type", "is_active", "display_order"),
        }),
    )
