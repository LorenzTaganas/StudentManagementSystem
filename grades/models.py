from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from accounts.models import User
from courses.models import Subject, Enrollment

class Grade(models.Model):
    """
    Stores grades for students in each subject
    Supports prelim, midterm, and final grades with weighted average calculation
    """
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='grade')
    
    # Grade components (0-100 scale)
    prelim_grade = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Prelim grade (0-100)"
    )
    midterm_grade = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Midterm grade (0-100)"
    )
    final_grade = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Final grade (0-100)"
    )
    
    # Weighted percentages (must sum to 100)
    prelim_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=30.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Prelim weight percentage"
    )
    midterm_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=30.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Midterm weight percentage"
    )
    final_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=40.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Final weight percentage"
    )
    
    # Computed fields
    weighted_average = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Computed weighted average"
    )
    letter_grade = models.CharField(max_length=2, blank=True, null=True)
    grade_point = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
    
    def clean(self):
        """Validate that weights sum to 100"""
        total_weight = (self.prelim_weight or 0) + (self.midterm_weight or 0) + (self.final_weight or 0)
        if total_weight != 100:
            raise ValidationError(f"Grade weights must sum to 100%. Current sum: {total_weight}%")
    
    def calculate_weighted_average(self):
        """Calculate weighted average if all grades are present"""
        if self.prelim_grade is not None and self.midterm_grade is not None and self.final_grade is not None:
            weighted = (
                (self.prelim_grade * self.prelim_weight / 100) +
                (self.midterm_grade * self.midterm_weight / 100) +
                (self.final_grade * self.final_weight / 100)
            )
            return round(weighted, 2)
        return None
    
    def get_letter_grade(self, average):
        """Convert numerical grade to letter grade"""
        if average is None:
            return None
        if average >= 97:
            return '1.00'
        elif average >= 94:
            return '1.25'
        elif average >= 91:
            return '1.50'
        elif average >= 88:
            return '1.75'
        elif average >= 85:
            return '2.00'
        elif average >= 82:
            return '2.25'
        elif average >= 79:
            return '2.50'
        elif average >= 76:
            return '2.75'
        elif average >= 75:
            return '3.00'
        else:
            return '5.00'  # Failed
    
    def get_grade_point(self, letter):
        """Convert letter grade to grade point"""
        if letter is None:
            return None
        grade_map = {
            '1.00': 4.00, '1.25': 3.75, '1.50': 3.50, '1.75': 3.25,
            '2.00': 3.00, '2.25': 2.75, '2.50': 2.50, '2.75': 2.25,
            '3.00': 2.00, '5.00': 0.00
        }
        return grade_map.get(letter, 0.00)
    
    def save(self, *args, **kwargs):
        """Auto-calculate weighted average, letter grade, and grade point on save"""
        self.weighted_average = self.calculate_weighted_average()
        if self.weighted_average:
            self.letter_grade = self.get_letter_grade(self.weighted_average)
            self.grade_point = self.get_grade_point(self.letter_grade)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.enrollment.student.username} - {self.enrollment.subject.code} - {self.weighted_average or 'N/A'}"


class GPA(models.Model):
    """
    Stores computed GPA for students per semester/year
    """
    SEMESTER_CHOICES = [
        ('1', 'First Semester'),
        ('2', 'Second Semester'),
        ('summer', 'Summer'),
    ]
    
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'student'},
        related_name='gpa_records'
    )
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    academic_year = models.CharField(max_length=20, help_text="e.g., 2024-2025")
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    total_units = models.IntegerField(default=0)
    computed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-academic_year', '-semester']
        verbose_name = 'GPA'
        verbose_name_plural = 'GPAs'
        unique_together = ['student', 'semester', 'academic_year']
    
    def __str__(self):
        return f"{self.student.username} - {self.academic_year} {self.get_semester_display()} - GPA: {self.gpa or 'N/A'}"

