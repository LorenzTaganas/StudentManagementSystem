from django.contrib import admin
from .models import Course, Subject, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin for Course/Program model"""
    list_display = ['code', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']
    
    fieldsets = (
        ('Program Information', {
            'fields': ('code', 'name', 'description'),
            'description': 'Course represents the degree program (e.g., BSCS, BSIT). Subjects specify year levels.'
        }),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin for Subject model"""
    list_display = ['code', 'name', 'course', 'semester', 'units', 'instructor']
    list_filter = ['course', 'semester', 'instructor']
    search_fields = ['code', 'name', 'description', 'course__name']
    ordering = ['course', 'semester', 'code']
    
    fieldsets = (
        ('Subject Information', {
            'fields': ('code', 'name', 'description', 'course', 'units')
        }),
        ('Academic Details', {
            'fields': ('semester', 'instructor'),
            'description': 'Semester and instructor assignment.'
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin for Enrollment model"""
    list_display = ['student', 'subject', 'status', 'enrolled_date']
    list_filter = ['status', 'subject__course', 'enrolled_date']
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'subject__code', 'subject__name']
    ordering = ['-enrolled_date']
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'subject', 'status')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subject':
            # If editing, get the student from the form data
            student_id = request.GET.get('student') or request.POST.get('student')
            from accounts.models import StudentProfile
            from .models import Subject
            if student_id:
                try:
                    student_profile = StudentProfile.objects.get(user_id=student_id)
                    # Only show subjects for the student's program
                    kwargs["queryset"] = Subject.objects.filter(course__name=student_profile.program)
                except StudentProfile.DoesNotExist:
                    kwargs["queryset"] = Subject.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

