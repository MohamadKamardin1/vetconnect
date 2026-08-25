from django.contrib import admin
from privacy.models import DataDeletionRequest, DataExportRequest


@admin.register(DataExportRequest)
class DataExportRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "requested_at", "completed_at")
    list_filter = ("status",)
    search_fields = ("user__email",)
    readonly_fields = ("id", "user", "status", "payload", "requested_at", "completed_at")


@admin.register(DataDeletionRequest)
class DataDeletionRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "requested_at", "completed_at")
    list_filter = ("status",)
    search_fields = ("user__email",)
