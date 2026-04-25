from django.contrib import admin

from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "employment_type", "location", "is_active", "display_order")
    list_display_links = ("title",)
    list_filter = ("is_active", "employment_type", "department")
    search_fields = ("title", "department", "location", "summary", "requirements")
    list_editable = ("is_active", "display_order")
    ordering = ("display_order", "-created_at")
