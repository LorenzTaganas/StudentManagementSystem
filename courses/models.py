from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

class Course(models.Model):
    """
    Represents a degree program (e.g., BS Computer Science, BS Information Technology)
    This is the 4-year program, NOT tied to a specific year level.
    Subjects within this course will specify which year level they belong to.
    """
    code = models.CharField(max_length=20, unique=True, help_text="e.g., BSCS, BSIT")
    name = models.CharField(max_length=200, help_text="e.g., BS Computer Science")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Course/Program'
        verbose_name_plural = 'Courses/Programs'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Subject(models.Model):
    """
    Represents individual subjects within a course/program.
    Example: IT101 - Systems Analysis and Modeling
    - Belongs to BSCS (course)
    - Taught in Year 1, First Semester
    - Worth 3 units
    - Assigned to an instructor
    """
    SEMESTER_CHOICES = [
        ('1', 'First Semester'),
        ('2', 'Second Semester'),
        ('summer', 'Summer'),
    ]
    
    code = models.CharField(max_length=20, unique=True, help_text="e.g., IT101, CS201")
    name = models.CharField(max_length=200, help_text="e.g., Systems Analysis and Modeling")
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='subjects',
        help_text="Which program this subject belongs to (e.g., BSCS, BSIT)"
    )
    units = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        default=3,
        help_text="Number of units (typically 1-6)"
    )
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1')
    instructor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': 'instructor'},
        related_name='subjects_taught'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'semester', 'code']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    """
    Tracks student enrollment in subjects
    """
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enrolled_date']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ['student', 'subject']
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.subject.code}"

