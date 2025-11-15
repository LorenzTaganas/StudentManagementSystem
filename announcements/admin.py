from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Admin for Announcement model"""
    list_display = ['title', 'announcement_type', 'subject', 'created_by', 'is_active', 'created_at']
    list_filter = ['announcement_type', 'is_active', 'created_at', 'subject__course']
    search_fields = ['title', 'content', 'subject__code', 'subject__name', 'created_by__username']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Announcement Information', {
            'fields': ('title', 'content', 'announcement_type', 'subject')
        }),
        ('Settings', {
            'fields': ('created_by', 'is_active')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user if not set"""
        if not obj.pk:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

