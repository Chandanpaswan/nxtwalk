from django.contrib import admin
from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("project", "industry", "is_published", "published_at")
    list_filter = ("industry", "is_published", "published_at")
    search_fields = ("project__title", "industry", "strategy", "results")
    autocomplete_fields = ("project",)
    list_select_related = ("project",)