from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "service", "is_read", "is_contacted", "created_at")
    list_filter = ("is_read", "is_contacted", "service", "created_at")
    search_fields = ("name", "email", "phone", "company", "subject", "message")
    list_select_related = ("service",)
    list_per_page = 30
    actions = ("mark_read", "mark_contacted")

    @admin.action(description="Mark selected messages as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(is_contacted=True)
