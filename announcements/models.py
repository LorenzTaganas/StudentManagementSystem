from django.db import models
from accounts.models import User
from courses.models import Subject

class Announcement(models.Model):
    """
    System-wide and course-specific announcements
    Can be created by admin or instructors
    """
    ANNOUNCEMENT_TYPE_CHOICES = [
        ('system', 'System-wide'),
        ('course', 'Course-specific'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPE_CHOICES, default='system')
    
    # If course-specific, link to subject
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='announcements',
        help_text="Leave blank for system-wide announcements"
    )
    
    # Creator (admin or instructor)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='announcements_created'
    )
    
    # Visibility
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this announcement")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def __str__(self):
        type_str = f"[{self.get_announcement_type_display()}]"
        subject_str = f" - {self.subject.code}" if self.subject else ""
        return f"{type_str} {self.title}{subject_str}"
    
    def clean(self):
        """Validate that course-specific announcements have a subject"""
        from django.core.exceptions import ValidationError
        if self.announcement_type == 'course' and not self.subject:
            raise ValidationError("Course-specific announcements must have a subject selected.")
        if self.announcement_type == 'system' and self.subject:
            raise ValidationError("System-wide announcements should not have a subject selected.")

