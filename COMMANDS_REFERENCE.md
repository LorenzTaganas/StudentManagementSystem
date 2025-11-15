# 🛠️ Useful Django Commands Reference

## Basic Commands

### Start Development Server
```bash
python manage.py runserver
```
Access at: http://127.0.0.1:8000/

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
# Create migration files after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Show migrations status
python manage.py showmigrations
```

---

## Database Commands

### Open Django Shell
```bash
python manage.py shell
```

### Example Shell Commands
```python
# Import models
from accounts.models import User, StudentProfile, InstructorProfile
from courses.models import Course, Subject, Enrollment
from grades.models import Grade, GPA
from announcements.models import Announcement

# Get all users
User.objects.all()

# Get all students
User.objects.filter(role='student')

# Get specific user
user = User.objects.get(username='student1')

# Create a student programmatically
student = User.objects.create_user(
    username='student2',
    email='student2@example.com',
    password='password123',
    role='student',
    first_name='John',
    last_name='Doe'
)

# Create student profile
profile = StudentProfile.objects.create(
    user=student,
    student_id='2024-002',
    year_level='1',
    program='BS Computer Science'
)

# Get student's enrollments
enrollments = Enrollment.objects.filter(student=student)

# Get student's grades
grades = Grade.objects.filter(enrollment__student=student)

# Calculate average grade
from django.db.models import Avg
avg = Grade.objects.filter(
    enrollment__student=student
).aggregate(avg_grade=Avg('weighted_average'))
```

---

## Data Management

### Dump Data (Backup)
```bash
# Export all data to JSON
python manage.py dumpdata > backup.json

# Export specific app
python manage.py dumpdata accounts > accounts_backup.json
python manage.py dumpdata courses > courses_backup.json
python manage.py dumpdata grades > grades_backup.json
```

### Load Data (Restore)
```bash
python manage.py loaddata backup.json
```

### Reset Database (CAREFUL!)
```bash
# Delete database
rm db.sqlite3

# Delete all migrations (optional, usually not needed)
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Recreate migrations and database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## App Management

### Create New App
```bash
python manage.py startapp app_name
```

Then add to INSTALLED_APPS in settings.py

---

## Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test courses
python manage.py test grades

# Run specific test case
python manage.py test accounts.tests.UserModelTest
```

---

## Static Files

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

---

## User Management Commands

### Change User Password
```bash
python manage.py changepassword username
```

### Create Superuser Without Interactive Prompt
```bash
python manage.py createsuperuser --username admin --email admin@example.com --noinput
```

---

## Database Inspection

### Show SQL for Migration
```bash
python manage.py sqlmigrate accounts 0001
```

### Check for Model Problems
```bash
python manage.py check
```

### Show Database Schema
```bash
python manage.py inspectdb
```

---

## Useful Shell Queries

### Get All Courses with Subject Count
```python
from courses.models import Course
from django.db.models import Count

courses = Course.objects.annotate(
    subject_count=Count('subjects')
)

for course in courses:
    print(f"{course.name}: {course.subject_count} subjects")
```

### Get Instructor's Subjects
```python
from accounts.models import User

instructor = User.objects.get(username='instructor1')
subjects = instructor.subjects_taught.all()

for subject in subjects:
    print(f"{subject.code} - {subject.name}")
```

### Get Student's Grades with Details
```python
from accounts.models import User
from grades.models import Grade

student = User.objects.get(username='student1')
grades = Grade.objects.filter(enrollment__student=student).select_related(
    'enrollment__subject',
    'enrollment__subject__course'
)

for grade in grades:
    subject = grade.enrollment.subject
    print(f"{subject.code}: {grade.weighted_average} ({grade.letter_grade})")
```

### Calculate Student's GPA
```python
from django.db.models import Avg, Sum
from accounts.models import User

student = User.objects.get(username='student1')

# Get all completed enrollments with grades
enrollments = student.enrollments.filter(
    status='completed',
    grade__isnull=False
).select_related('subject', 'grade')

total_points = 0
total_units = 0

for enrollment in enrollments:
    units = enrollment.subject.units
    grade_point = enrollment.grade.grade_point
    total_points += (grade_point * units)
    total_units += units

gpa = total_points / total_units if total_units > 0 else 0
print(f"GPA: {gpa:.2f}")
```

### Get All Active Announcements
```python
from announcements.models import Announcement
from django.utils import timezone

# System-wide announcements
system_announcements = Announcement.objects.filter(
    announcement_type='system',
    is_active=True
).order_by('-created_at')

# Course-specific announcements for a student
student = User.objects.get(username='student1')
enrolled_subjects = student.enrollments.filter(
    status='enrolled'
).values_list('subject', flat=True)

course_announcements = Announcement.objects.filter(
    announcement_type='course',
    subject__in=enrolled_subjects,
    is_active=True
).order_by('-created_at')
```

---

## Debugging

### Enable SQL Query Logging
In settings.py, add:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

### Check Django Version
```bash
python manage.py --version
```

### Show Settings
```bash
python manage.py diffsettings
```

---

## Production Readiness

### Check Deployment Checklist
```bash
python manage.py check --deploy
```

### Create Requirements File
```bash
pip freeze > requirements.txt
```

### Install from Requirements
```bash
pip install -r requirements.txt
```

---

## Quick Data Population Script

Create a file `populate_data.py` in project root:

```python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentGradeManagementSystem.settings')

import django
django.setup()

from accounts.models import User, StudentProfile, InstructorProfile
from courses.models import Course, Subject, Enrollment
from grades.models import Grade

# Create instructor
instructor = User.objects.create_user(
    username='prof_smith',
    password='password123',
    role='instructor',
    first_name='John',
    last_name='Smith',
    email='smith@university.edu'
)
InstructorProfile.objects.create(
    user=instructor,
    employee_id='INST-001',
    department='Computer Science'
)

# Create course
course = Course.objects.create(
    code='BSCS',
    name='Bachelor of Science in Computer Science',
    year_level=1,
    description='4-year CS program'
)

# Create subject
subject = Subject.objects.create(
    code='CS101',
    name='Introduction to Programming',
    course=course,
    units=3,
    semester='1',
    year_level=1,
    instructor=instructor
)

# Create students
for i in range(1, 6):
    student = User.objects.create_user(
        username=f'student{i}',
        password='password123',
        role='student',
        first_name=f'Student',
        last_name=f'Number{i}',
        email=f'student{i}@university.edu'
    )
    StudentProfile.objects.create(
        user=student,
        student_id=f'2024-00{i}',
        year_level='1',
        program='BS Computer Science'
    )
    
    # Enroll in subject
    enrollment = Enrollment.objects.create(
        student=student,
        subject=subject,
        status='enrolled'
    )
    
    # Add grades
    Grade.objects.create(
        enrollment=enrollment,
        prelim_grade=85 + i,
        midterm_grade=88 + i,
        final_grade=90 + i
    )

print("Sample data created successfully!")
```

Run with:
```bash
python populate_data.py
```

---

## Common Issues & Solutions

### Issue: "No module named 'X'"
```bash
pip install package_name
```

### Issue: Migrations conflict
```bash
python manage.py migrate --fake
```

### Issue: Can't access admin CSS
```bash
python manage.py collectstatic
```

### Issue: Permission denied on media files
```bash
# On Linux/Mac
chmod -R 755 media/

# Or set in settings.py
FILE_UPLOAD_PERMISSIONS = 0o644
```

---

**Pro Tip**: Create a `Makefile` or batch script for common commands!

Example `run.bat`:
```batch
@echo off
echo Starting Django Development Server...
python manage.py runserver
```

Example `Makefile`:
```makefile
.PHONY: run migrate shell test

run:
    python manage.py runserver

migrate:
    python manage.py makemigrations
    python manage.py migrate

shell:
    python manage.py shell

test:
    python manage.py test

superuser:
    python manage.py createsuperuser
```

Then just run:
```bash
make run
make migrate
make test
```
