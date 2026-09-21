from django.contrib import admin
from .models import Grade, GPA

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """Admin for Grade model"""
    list_display = ['get_student', 'get_subject', 'prelim_grade', 'midterm_grade', 'final_grade', 'weighted_average', 'letter_grade']
    list_filter = ['enrollment__subject__course', 'enrollment__subject', 'letter_grade']
    search_fields = ['enrollment__student__username', 'enrollment__student__first_name', 'enrollment__student__last_name', 'enrollment__subject__code']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Enrollment', {
            'fields': ('enrollment',)
        }),
        ('Grades', {
            'fields': ('prelim_grade', 'midterm_grade', 'final_grade')
        }),
        ('Weights', {
            'fields': ('prelim_weight', 'midterm_weight', 'final_weight'),
            'description': 'Grade weights must sum to 100%'
        }),
        ('Computed Results', {
            'fields': ('weighted_average', 'letter_grade', 'grade_point'),
            'description': 'These fields are automatically calculated'
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
    )
    
    readonly_fields = ['weighted_average', 'letter_grade', 'grade_point']
    
    def get_student(self, obj):
        return obj.enrollment.student.username
    get_student.short_description = 'Student'
    get_student.admin_order_field = 'enrollment__student__username'
    
    def get_subject(self, obj):
        return obj.enrollment.subject.code
    get_subject.short_description = 'Subject'
    get_subject.admin_order_field = 'enrollment__subject__code'


@admin.register(GPA)
class GPAAdmin(admin.ModelAdmin):
    """Admin for GPA model"""
    list_display = ['student', 'semester', 'academic_year', 'gpa', 'total_units', 'computed_at']
    list_filter = ['semester', 'academic_year']
    search_fields = ['student__username', 'student__first_name', 'student__last_name']
    ordering = ['-academic_year', '-semester']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Academic Period', {
            'fields': ('semester', 'academic_year')
        }),
        ('Results', {
            'fields': ('gpa', 'total_units')
        }),
    )

