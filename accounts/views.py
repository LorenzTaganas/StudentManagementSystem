def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')
def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, 'Registration successful! Please log in to continue.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import User, StudentProfile, InstructorProfile
from django import forms

# Registration Form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('student', 'Student'),
            ('instructor', 'Instructor'),
        ]

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data


# Profile Forms
class StudentProfileForm(forms.ModelForm):
    from courses.models import Course
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by('name'),
        empty_label="Select your program/course",
        label="Program",
        help_text="Select your degree program (e.g., BS Computer Science)"
    )
    
    class Meta:
        model = StudentProfile
        fields = ['course']





@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    """Role-based dashboard redirect"""
    if request.user.is_student:
        return redirect('accounts:student_dashboard')
    elif request.user.is_instructor:
        return redirect('accounts:instructor_dashboard')
    else:
        # Redirect admins to Django's built-in admin panel
        return redirect('/admin/')


@login_required
def student_dashboard(request):
    """Student dashboard"""
    if not request.user.is_student:
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    # Get student's enrollments and grades
    from django.db import models
    from courses.models import Enrollment
    from grades.models import Grade
    from announcements.models import Announcement
    
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status='enrolled'
    ).select_related('subject', 'subject__course', 'subject__instructor')
    
    # Get grades
    grades = Grade.objects.filter(
        enrollment__student=request.user
    ).select_related('enrollment__subject').order_by('-created_at')[:5]
    
    # Calculate GPA
    completed_grades = Grade.objects.filter(
        enrollment__student=request.user,
        enrollment__status='completed',
        grade_point__isnull=False
    )
    
    total_points = 0
    total_units = 0
    for grade in completed_grades:
        units = grade.enrollment.subject.units
        total_points += (grade.grade_point * units)
        total_units += units
    
    gpa = round(total_points / total_units, 2) if total_units > 0 else 0
    
    # Get announcements
    enrolled_subjects = enrollments.values_list('subject', flat=True)
    announcements = Announcement.objects.filter(
        is_active=True
    ).filter(
        models.Q(announcement_type='system') |
        models.Q(subject__in=enrolled_subjects)
    ).order_by('-created_at')[:5]
    
    context = {
        'enrollments': enrollments,
        'grades': grades,
        'gpa': gpa,
        'announcements': announcements,
        'total_enrollments': enrollments.count(),
    }
    
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
def instructor_dashboard(request):
    """Instructor dashboard"""
    if not request.user.is_instructor:
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    
    from courses.models import Subject, Enrollment
    from announcements.models import Announcement
    
    # Get instructor's subjects
    subjects = Subject.objects.filter(instructor=request.user)
    
    # Get total students across all subjects
    total_students = Enrollment.objects.filter(
        subject__instructor=request.user,
        status='enrolled'
    ).values('student').distinct().count()
    
    # Get recent announcements
    announcements = Announcement.objects.filter(
        created_by=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'subjects': subjects,
        'total_subjects': subjects.count(),
        'total_students': total_students,
        'announcements': announcements,
    }
    
    return render(request, 'accounts/instructor_dashboard.html', context)





@login_required
def complete_student_profile(request):
    """Complete student profile after registration"""
    if not request.user.is_student:
        return redirect('dashboard')
    
    # Check if profile already exists
    if hasattr(request.user, 'student_profile'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            
            # Set the program from the selected course
            profile.program = form.cleaned_data['course'].name
            
            # Auto-generate student ID
            from datetime import datetime
            year = datetime.now().year
            # Get the count of existing students + 1 for unique ID
            student_count = StudentProfile.objects.count() + 1
            profile.student_id = f"{year}{student_count:06d}"  # Format: 2025000001
            
            profile.save()
            messages.success(request, f'Profile completed successfully! Your Student ID is: {profile.student_id}')
            return redirect('dashboard')
    else:
        form = StudentProfileForm()
    
    return render(request, 'accounts/complete_student_profile.html', {'form': form})


@login_required
def complete_instructor_profile(request):
    """Complete instructor profile after registration"""
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    # Check if profile already exists
    if hasattr(request.user, 'instructor_profile'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = InstructorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # Auto-generate employee_id
            last_inst = InstructorProfile.objects.order_by('-id').first()
            if last_inst and last_inst.employee_id:
                last_id = int(last_inst.employee_id.split('-')[1]) if '-' in last_inst.employee_id else last_inst.id
                new_id = f"INST-{last_id + 1:03d}"
            else:
                new_id = "INST-001"
            profile.employee_id = new_id
            # Set hire_date automatically
            from datetime import date
            profile.hire_date = date.today()
            profile.save()
            messages.success(request, f'Profile completed! Your Employee ID is: {profile.employee_id}')
            return redirect('dashboard')
    else:
        form = InstructorProfileForm()
    return render(request, 'accounts/complete_instructor_profile.html', {'form': form})


@login_required
def profile(request):
    """User profile view with edit functionality"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            # Handle profile picture upload separately
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()
                messages.success(request, 'Profile picture updated successfully!')
                return redirect('accounts:profile')
            
            # Update basic info only if form fields are present
            if 'first_name' in request.POST:
                request.user.first_name = request.POST.get('first_name', '')
                request.user.last_name = request.POST.get('last_name', '')
                request.user.email = request.POST.get('email', '')
                request.user.phone_number = request.POST.get('phone_number', '')
                request.user.address = request.POST.get('address', '')
                request.user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        
        elif action == 'remove_photo':
            # Remove profile picture and revert to default
            if request.user.profile_picture:
                request.user.profile_picture.delete(save=False)
                request.user.profile_picture = None
                request.user.save()
                messages.success(request, 'Profile picture removed successfully!')
            return redirect('accounts:profile')
        
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not request.user.check_password(old_password):
                messages.error(request, 'Current password is incorrect')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters')
            else:
                request.user.set_password(new_password)
                request.user.save()
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
                return redirect('accounts:profile')
        
        elif action == 'delete_account':
            password = request.POST.get('password_confirm')
            if request.user.check_password(password):
                request.user.delete()
                messages.success(request, 'Your account has been deleted')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Incorrect password')
    
    return render(request, 'accounts/profile.html')


@login_required
def view_all_grades(request):
    """View all grades with detailed information"""
    if not request.user.is_student:
        messages.error(request, 'Access denied. Students only.')
        return redirect('accounts:dashboard')
    
    from courses.models import Enrollment
    from grades.models import Grade
    
    # Get all grades for the student
    grades = Grade.objects.filter(
        enrollment__student=request.user
    ).select_related(
        'enrollment__subject',
        'enrollment__subject__course',
        'enrollment__subject__instructor'
    ).order_by('-enrollment__enrolled_date')
    
    # Calculate overall statistics
    total_subjects = grades.count()
    completed_grades = grades.filter(weighted_average__isnull=False)
    
    # Calculate GPA
    total_points = 0
    total_units = 0
    for grade in completed_grades:
        if grade.grade_point is not None:
            units = grade.enrollment.subject.units
            total_points += (grade.grade_point * units)
            total_units += units
    
    gpa = round(total_points / total_units, 2) if total_units > 0 else 0
    
    # Calculate passed/failed count
    passed = completed_grades.exclude(letter_grade='5.00').count()
    failed = completed_grades.filter(letter_grade='5.00').count()
    incomplete = total_subjects - completed_grades.count()
    
    context = {
        'grades': grades,
        'total_subjects': total_subjects,
        'gpa': gpa,
        'passed': passed,
        'failed': failed,
        'incomplete': incomplete,
    }
    
    return render(request, 'accounts/view_all_grades.html', context)


@login_required
def view_all_announcements(request):
    """View all announcements for students"""
    if not request.user.is_student:
        messages.error(request, 'Access denied. Students only.')
        return redirect('accounts:dashboard')
    
    from django.db import models
    from courses.models import Enrollment
    from announcements.models import Announcement
    
    # Get student's enrolled subjects
    enrolled_subjects = Enrollment.objects.filter(
        student=request.user,
        status='enrolled'
    ).values_list('subject', flat=True)
    
    # Get all relevant announcements
    announcements = Announcement.objects.filter(
        is_active=True
    ).filter(
        models.Q(announcement_type='system') |
        models.Q(subject__in=enrolled_subjects)
    ).select_related('subject', 'created_by').order_by('-created_at')
    
    context = {
        'announcements': announcements,
    }
    
    return render(request, 'accounts/view_all_announcements.html', context)


