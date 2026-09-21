from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject, Enrollment
from grades.models import Grade

@login_required
def subject_students(request, subject_id):
    """View students enrolled in a subject (for instructors)"""
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Ensure only the assigned instructor can view
    if not request.user.is_instructor or subject.instructor != request.user:
        messages.error(request, 'You do not have permission to view this subject.')
        return redirect('accounts:dashboard')
    
    # Get all enrollments for this subject
    enrollments = Enrollment.objects.filter(
        subject=subject,
        status='enrolled'
    ).select_related('student', 'student__student_profile').prefetch_related('grade')
    
    # Prepare student data with grades
    students_data = []
    for enrollment in enrollments:
        # Get or create grade record
        grade, created = Grade.objects.get_or_create(enrollment=enrollment)
        
        students_data.append({
            'enrollment': enrollment,
            'student': enrollment.student,
            'student_profile': enrollment.student.student_profile if hasattr(enrollment.student, 'student_profile') else None,
            'grade': grade,
        })
    
    context = {
        'subject': subject,
        'students_data': students_data,
        'total_students': len(students_data),
    }
    
    return render(request, 'courses/subject_students.html', context)

@login_required
def subject_list(request):
    """View all subjects for the current user (student or instructor)"""
    if request.user.is_instructor:
        subjects = Subject.objects.filter(instructor=request.user)
    elif request.user.is_student:
        subjects = Subject.objects.filter(enrollments__student=request.user).distinct()
    else:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    context = {
        'subjects': subjects,
        'total_subjects': subjects.count(),
    }
    return render(request, 'courses/subject_list.html', context)
