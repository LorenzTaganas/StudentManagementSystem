from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Supports three roles: Admin, Instructor, and Student
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_admin_role(self):
        return self.role == 'admin'


class StudentProfile(models.Model):
    """
    Extended profile for students
    Stores student-specific information like student ID and program
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    enrolled_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['student_id']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name() or self.user.username}"


class InstructorProfile(models.Model):
    """
    Extended profile for instructors
    Stores instructor-specific information like employee ID, department, etc.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Instructor Profile'
        verbose_name_plural = 'Instructor Profiles'
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

