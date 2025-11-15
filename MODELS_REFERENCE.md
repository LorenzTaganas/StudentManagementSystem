# 📊 Database Models Overview

## Model Relationships Diagram

```
User (Custom User Model)
├── role: admin/instructor/student
├── profile_picture: ImageField
├── phone_number, address, date_of_birth
│
├─[ONE-TO-ONE]─→ StudentProfile
│                 └── student_id, year_level, program
│
├─[ONE-TO-ONE]─→ InstructorProfile
│                 └── employee_id, department, specialization
│
├─[ONE-TO-MANY]─→ Enrollment (as student)
│                 └── status: enrolled/dropped/completed
│
├─[ONE-TO-MANY]─→ Subject (as instructor)
│
├─[ONE-TO-MANY]─→ GPA
│
└─[ONE-TO-MANY]─→ Announcement (as created_by)

Course
├── code, name, description, year_level
│
└─[ONE-TO-MANY]─→ Subject
                   ├── code, name, units, semester
                   ├─[MANY-TO-ONE]─→ Course
                   ├─[MANY-TO-ONE]─→ User (instructor)
                   │
                   ├─[ONE-TO-MANY]─→ Enrollment
                   │                 ├─[MANY-TO-ONE]─→ User (student)
                   │                 │
                   │                 └─[ONE-TO-ONE]─→ Grade
                   │                                   ├── prelim_grade
                   │                                   ├── midterm_grade
                   │                                   ├── final_grade
                   │                                   ├── weighted_average (auto)
                   │                                   ├── letter_grade (auto)
                   │                                   └── grade_point (auto)
                   │
                   └─[ONE-TO-MANY]─→ Announcement (course-specific)
```

## Detailed Model Breakdown

### 1. accounts.User (Custom User)
**Extends**: Django's AbstractUser  
**Purpose**: Central user model with role-based access  

| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Unique username (inherited) |
| email | EmailField | Email address (inherited) |
| password | CharField | Hashed password (inherited) |
| first_name | CharField | First name (inherited) |
| last_name | CharField | Last name (inherited) |
| **role** | CharField | admin/instructor/student |
| phone_number | CharField | Contact number with validation |
| profile_picture | ImageField | Uploaded to `media/profile_pictures/` |
| date_of_birth | DateField | Birth date |
| address | TextField | Full address |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

**Methods**:
- `is_student` - Check if user is student
- `is_instructor` - Check if user is instructor  
- `is_admin_role` - Check if user is admin

---

### 2. accounts.StudentProfile
**Purpose**: Extended profile for students  
**Relationship**: One-to-One with User

| Field | Type | Description |
|-------|------|-------------|
| user | OneToOneField | Link to User (role=student) |
| student_id | CharField | Unique student ID |
| year_level | CharField | 1/2/3/4 (First to Fourth Year) |
| program | CharField | e.g., "BS Computer Science" |
| enrolled_date | DateField | Auto timestamp |

---

### 3. accounts.InstructorProfile
**Purpose**: Extended profile for instructors  
**Relationship**: One-to-One with User

| Field | Type | Description |
|-------|------|-------------|
| user | OneToOneField | Link to User (role=instructor) |
| employee_id | CharField | Unique employee ID |
| department | CharField | e.g., "Computer Science" |
| specialization | CharField | Area of expertise |
| hire_date | DateField | Date hired |

---

### 4. courses.Course
**Purpose**: Represents academic programs  

| Field | Type | Description |
|-------|------|-------------|
| code | CharField | Unique course code (e.g., BSCS) |
| name | CharField | Full name |
| description | TextField | Course description |
| year_level | IntegerField | Target year (1-4) |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

---

### 5. courses.Subject
**Purpose**: Individual subjects within courses  
**Relationships**: 
- Many-to-One with Course
- Many-to-One with User (instructor)

| Field | Type | Description |
|-------|------|-------------|
| code | CharField | Unique subject code (e.g., CS101) |
| name | CharField | Subject name |
| description | TextField | Subject description |
| course | ForeignKey | Parent course |
| units | IntegerField | Credit units (1-6) |
| semester | CharField | 1/2/summer |
| year_level | IntegerField | Year level (1-4) |
| instructor | ForeignKey | Assigned instructor (User) |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

---

### 6. courses.Enrollment
**Purpose**: Tracks student enrollment in subjects  
**Relationships**:
- Many-to-One with User (student)
- Many-to-One with Subject
- **Unique Together**: (student, subject)

| Field | Type | Description |
|-------|------|-------------|
| student | ForeignKey | Enrolled student (User) |
| subject | ForeignKey | Enrolled subject |
| status | CharField | enrolled/dropped/completed |
| enrolled_date | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

---

### 7. grades.Grade
**Purpose**: Stores and calculates student grades  
**Relationship**: One-to-One with Enrollment

| Field | Type | Description |
|-------|------|-------------|
| enrollment | OneToOneField | Link to enrollment |
| prelim_grade | DecimalField | Prelim grade (0-100) |
| midterm_grade | DecimalField | Midterm grade (0-100) |
| final_grade | DecimalField | Final grade (0-100) |
| prelim_weight | DecimalField | Weight % (default 30) |
| midterm_weight | DecimalField | Weight % (default 30) |
| final_weight | DecimalField | Weight % (default 40) |
| **weighted_average** | DecimalField | **AUTO-CALCULATED** |
| **letter_grade** | CharField | **AUTO-CALCULATED** (1.00-5.00) |
| **grade_point** | DecimalField | **AUTO-CALCULATED** (0.00-4.00) |
| remarks | TextField | Optional notes |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

**Auto-Calculation Logic**:
```python
weighted_average = (prelim * 0.30) + (midterm * 0.30) + (final * 0.40)

# Letter Grade Conversion:
97-100  → 1.00 (4.00 GPA)
94-96   → 1.25 (3.75 GPA)
91-93   → 1.50 (3.50 GPA)
88-90   → 1.75 (3.25 GPA)
85-87   → 2.00 (3.00 GPA)
82-84   → 2.25 (2.75 GPA)
79-81   → 2.50 (2.50 GPA)
76-78   → 2.75 (2.25 GPA)
75      → 3.00 (2.00 GPA)
<75     → 5.00 (0.00 GPA - Failed)
```

**Methods**:
- `calculate_weighted_average()` - Computes weighted avg
- `get_letter_grade(average)` - Converts to letter grade
- `get_grade_point(letter)` - Converts to GPA scale
- `save()` - Overridden to auto-calculate on save

**Validation**:
- `clean()` - Ensures weights sum to 100%

---

### 8. grades.GPA
**Purpose**: Stores computed GPA per semester  
**Relationship**: Many-to-One with User (student)  
**Unique Together**: (student, semester, academic_year)

| Field | Type | Description |
|-------|------|-------------|
| student | ForeignKey | Student (User) |
| semester | CharField | 1/2/summer |
| academic_year | CharField | e.g., "2024-2025" |
| gpa | DecimalField | Computed GPA (0.00-4.00) |
| total_units | IntegerField | Total units taken |
| computed_at | DateTimeField | Auto timestamp |

---

### 9. announcements.Announcement
**Purpose**: System-wide and course-specific announcements  
**Relationships**:
- Many-to-One with User (created_by)
- Many-to-One with Subject (optional)

| Field | Type | Description |
|-------|------|-------------|
| title | CharField | Announcement title |
| content | TextField | Full content |
| announcement_type | CharField | system/course |
| subject | ForeignKey | Optional (for course-specific) |
| created_by | ForeignKey | Creator (admin/instructor) |
| is_active | BooleanField | Visibility toggle |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

**Validation**:
- `clean()` - Ensures course announcements have subject

---

## Key Features by Model

### Automatic Calculations
- **Grade Model**: Auto-calculates weighted average, letter grade, and GPA
- **GPA Model**: Tracks semester and cumulative GPA

### Validation Rules
- Grade weights must sum to 100%
- Grades must be 0-100
- Course announcements must have a subject
- System announcements cannot have a subject
- Phone number format validation

### Unique Constraints
- User: username, email
- StudentProfile: student_id
- InstructorProfile: employee_id
- Course: code
- Subject: code
- Enrollment: (student, subject)
- GPA: (student, semester, academic_year)

### Cascading Deletes
- Deleting a User deletes their profiles
- Deleting a Course deletes all subjects
- Deleting a Subject deletes enrollments
- Deleting an Enrollment deletes the grade
- Instructor deletion: SET_NULL on subjects

---

## Query Examples

### Get all students
```python
from accounts.models import User
students = User.objects.filter(role='student')
```

### Get student's grades
```python
from grades.models import Grade
student = User.objects.get(username='student1')
grades = Grade.objects.filter(enrollment__student=student)
```

### Get instructor's subjects
```python
instructor = User.objects.get(username='instructor1')
subjects = instructor.subjects_taught.all()
```

### Get course subjects
```python
from courses.models import Course
course = Course.objects.get(code='BSCS')
subjects = course.subjects.all()
```

### Get active system announcements
```python
from announcements.models import Announcement
announcements = Announcement.objects.filter(
    announcement_type='system',
    is_active=True
)
```

### Calculate student GPA for a semester
```python
from django.db.models import Avg
enrollments = student.enrollments.filter(
    subject__semester='1',
    status='completed'
)
avg_gpa = enrollments.aggregate(
    avg_grade=Avg('grade__grade_point')
)
```

---

**Total Models**: 9  
**Apps**: 4 (accounts, courses, grades, announcements)  
**Database**: SQLite (dev) / PostgreSQL (prod recommended)
