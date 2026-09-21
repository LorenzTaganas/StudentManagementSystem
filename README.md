# Student Grade Management System - Backend

A comprehensive Django-based backend system for managing student grades, courses, and academic information.

## 🎯 Features

### 1. **Accounts App** (User Management)
- Custom User model with role-based access (Admin, Instructor, Student)
- Student profiles with student ID, year level, and program information
- Instructor profiles with employee ID, department, and specialization
- User authentication and authorization
- Profile picture upload support
- Phone number and address fields

### 2. **Courses App** (Course Management)
- Course management (BS Computer Science, etc.)
- Subject management with units, semester, and year level
- Instructor assignment to subjects
- Student enrollment tracking
- Enrollment status (Enrolled, Dropped, Completed)

### 3. **Grades App** (Grading System)
- Grade entry for Prelim, Midterm, and Final periods
- Configurable grade weights (default: 30%, 30%, 40%)
- Automatic weighted average calculation
- Letter grade conversion (1.00 to 5.00 scale)
- Grade point calculation for GPA
- Semester and yearly GPA tracking
- Grade validation and integrity checks

### 4. **Announcements App**
- System-wide announcements (for all users)
- Course-specific announcements (per subject)
- Instructor and admin announcement creation
- Active/inactive status for visibility control
- Timestamp tracking

## 📊 Database Schema

### User Model
- Extended from Django's AbstractUser
- Fields: username, email, password, role, phone_number, profile_picture, date_of_birth, address
- Roles: admin, instructor, student

### StudentProfile
- One-to-One with User
- Fields: student_id, year_level, program, enrolled_date

### InstructorProfile
- One-to-One with User
- Fields: employee_id, department, specialization, hire_date

### Course
- Fields: code, name, description, year_level

### Subject
- Fields: code, name, description, course, units, semester, year_level, instructor
- Foreign Key: Course, User (instructor)

### Enrollment
- Fields: student, subject, status, enrolled_date
- Foreign Keys: User (student), Subject

### Grade
- Fields: enrollment, prelim_grade, midterm_grade, final_grade, weights, weighted_average, letter_grade, grade_point
- Foreign Key: Enrollment
- Auto-calculates: weighted_average, letter_grade, grade_point

### GPA
- Fields: student, semester, academic_year, gpa, total_units
- Foreign Key: User (student)

### Announcement
- Fields: title, content, announcement_type, subject, created_by, is_active
- Foreign Keys: Subject (optional), User (created_by)

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Navigate to project directory**
   ```bash
   cd StudentGradeManagementSystem
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations** (Already done)
   ```bash
   python manage.py migrate
   ```

4. **Create superuser** (Admin account)
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

6. **Access Django Admin**
   - Open browser: http://127.0.0.1:8000/admin/
   - Login with superuser credentials

## 🔐 User Roles

### Admin
- Full system access via Django Admin
- Manage all users, courses, subjects, enrollments, grades
- Create system-wide announcements
- View all reports and analytics

### Instructor
- Manage assigned subjects
- Enter and update grades for enrolled students
- Create course-specific announcements
- View student rosters

### Student
- View own grades and GPA
- View enrolled subjects
- View announcements
- Access grade portal

## 📝 Grading System

### Grade Scale
| Percentage | Letter Grade | Grade Point |
|-----------|--------------|-------------|
| 97-100    | 1.00        | 4.00        |
| 94-96     | 1.25        | 3.75        |
| 91-93     | 1.50        | 3.50        |
| 88-90     | 1.75        | 3.25        |
| 85-87     | 2.00        | 3.00        |
| 82-84     | 2.25        | 2.75        |
| 79-81     | 2.50        | 2.50        |
| 76-78     | 2.75        | 2.25        |
| 75        | 3.00        | 2.00        |
| Below 75  | 5.00        | 0.00 (Failed) |

### Default Grade Weights
- Prelim: 30%
- Midterm: 30%
- Final: 40%

## 🛠️ Tech Stack
- **Framework**: Django 5.2.8
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **Language**: Python 3.13.7
- **Image Processing**: Pillow

## 📁 Project Structure
```
StudentGradeManagementSystem/
├── accounts/                 # User management app
│   ├── models.py            # User, StudentProfile, InstructorProfile
│   ├── admin.py             # Admin configurations
│   └── migrations/
├── courses/                  # Course management app
│   ├── models.py            # Course, Subject, Enrollment
│   ├── admin.py             # Admin configurations
│   └── migrations/
├── grades/                   # Grading system app
│   ├── models.py            # Grade, GPA
│   ├── admin.py             # Admin configurations
│   └── migrations/
├── announcements/           # Announcements app
│   ├── models.py            # Announcement
│   ├── admin.py             # Admin configurations
│   └── migrations/
├── StudentGradeManagementSystem/  # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configurations
│   └── wsgi.py
├── manage.py                # Django management script
├── db.sqlite3               # Database file
└── requirements.txt         # Python dependencies
```

## 🎓 Next Steps (Frontend Development)

Once the backend is complete, you can proceed with frontend development:

1. Create templates for each app
2. Build views for user dashboards
3. Implement authentication forms (login, registration)
4. Create grade entry interfaces for instructors
5. Build student grade portal
6. Design announcement boards
7. Implement profile management pages

## 📋 Admin Interface Access

After creating a superuser, you can access the Django Admin to:
- Create courses and subjects
- Add users (students, instructors)
- Enroll students in subjects
- Enter grades
- Post announcements
- View reports

## 🔒 Security Features
- Password validation
- CSRF protection
- User authentication
- Role-based access control
- Input validation

## 📌 Important Notes

1. **Custom User Model**: This project uses a custom User model (`accounts.User`). This is defined in `settings.py` as `AUTH_USER_MODEL = 'accounts.User'`.

2. **Media Files**: Profile pictures are stored in `media/profile_pictures/`. Ensure the `media/` directory exists and has proper permissions.

3. **Grade Calculation**: Grades are automatically calculated when saved. The weighted average, letter grade, and grade point are computed based on prelim, midterm, and final grades.

4. **Validation**: The system includes validation for:
   - Grade weights must sum to 100%
   - Grade values must be between 0-100
   - Course-specific announcements must have a subject

## 🐛 Testing

To test the backend:

1. Create test users with different roles
2. Add courses and subjects
3. Enroll students in subjects
4. Enter sample grades
5. Verify grade calculations
6. Test announcements

## 📞 Support

For issues or questions, refer to Django documentation: https://docs.djangoproject.com/

---

**Status**: Backend Complete ✅  
**Next**: Frontend Development
