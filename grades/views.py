from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Grade
from decimal import Decimal

@login_required
def edit_grade(request, grade_id):
    """Edit grades for a student in a subject"""
    grade = get_object_or_404(Grade, id=grade_id)
    subject = grade.enrollment.subject
    student = grade.enrollment.student
    
    # Ensure only the assigned instructor can edit grades
    if not request.user.is_instructor or subject.instructor != request.user:
        messages.error(request, 'You do not have permission to edit grades for this subject.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        try:
            # Get grade values from form
            prelim = request.POST.get('prelim_grade', '').strip()
            midterm = request.POST.get('midterm_grade', '').strip()
            final = request.POST.get('final_grade', '').strip()
            remarks = request.POST.get('remarks', '').strip()
            
            # Update grades (convert empty strings to None)
            grade.prelim_grade = Decimal(prelim) if prelim else None
            grade.midterm_grade = Decimal(midterm) if midterm else None
            grade.final_grade = Decimal(final) if final else None
            grade.remarks = remarks if remarks else None
            
            # Validate grade ranges
            for field, value in [('Prelim', grade.prelim_grade), ('Midterm', grade.midterm_grade), ('Final', grade.final_grade)]:
                if value is not None and (value < 0 or value > 100):
                    messages.error(request, f'{field} grade must be between 0 and 100.')
                    return redirect('grades:edit_grade', grade_id=grade_id)
            
            grade.save()  # This will auto-calculate weighted average and letter grade
            messages.success(request, f'Grades updated successfully for {student.get_full_name()}!')
            return redirect('courses:subject_students', subject_id=subject.id)
            
        except ValueError as e:
            messages.error(request, 'Invalid grade value. Please enter valid numbers.')
            return redirect('grades:edit_grade', grade_id=grade_id)
    
    context = {
        'grade': grade,
        'subject': subject,
        'student': student,
        'student_profile': student.student_profile if hasattr(student, 'student_profile') else None,
    }
    
    return render(request, 'grades/edit_grade.html', context)
