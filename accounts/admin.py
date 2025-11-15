from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, InstructorProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'profile_picture', 'date_of_birth', 'address')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'email', 'first_name', 'last_name', 'phone_number')
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin for Student Profile"""
    list_display = ['student_id', 'user', 'enrolled_date']
    list_filter = ['enrolled_date']
    search_fields = ['student_id', 'user__username', 'user__first_name', 'user__last_name']
    ordering = ['student_id']
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'student_id')
        }),
    )


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    """Admin for Instructor Profile"""
    list_display = ['employee_id', 'user', 'hire_date']
    list_filter = ['hire_date']
    search_fields = ['employee_id', 'user__username', 'user__first_name', 'user__last_name']
    ordering = ['employee_id']
    fieldsets = (
        ('Instructor Information', {
            'fields': ('user', 'employee_id', 'hire_date')
        }),
    )

