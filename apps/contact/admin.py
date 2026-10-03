from django.contrib import admin
from .models import ContactMessage, ProjectEnquiry


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "service", "status", "source", "created_at")
    list_filter = ("status", "service", "created_at")
    search_fields = ("name", "email", "phone", "company", "subject", "message", "admin_notes")
    list_select_related = ("service",)
    list_editable = ("status",)
    list_per_page = 30
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    actions = ("mark_new", "mark_contacted", "mark_qualified", "mark_converted", "mark_closed")

    @admin.action(description="Mark selected leads as new")
    def mark_new(self, request, queryset):
        queryset.update(status=ContactMessage.NEW)

    @admin.action(description="Mark selected leads as contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status=ContactMessage.CONTACTED)

    @admin.action(description="Mark selected leads as qualified")
    def mark_qualified(self, request, queryset):
        queryset.update(status=ContactMessage.QUALIFIED)

    @admin.action(description="Mark selected leads as converted")
    def mark_converted(self, request, queryset):
        queryset.update(status=ContactMessage.CONVERTED)

    @admin.action(description="Close selected leads")
    def mark_closed(self, request, queryset):
        queryset.update(status=ContactMessage.CLOSED)


@admin.register(ProjectEnquiry)
class ProjectEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "service", "budget", "status", "created_at")
    list_filter = ("status", "service", "budget", "created_at")
    search_fields = ("name", "email", "company", "phone", "message", "admin_notes")
    list_select_related = ("service",)
    list_editable = ("status",)
    list_per_page = 30
    date_hierarchy = "created_at"
