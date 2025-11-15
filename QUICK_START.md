# 🚀 Quick Start Guide

## Step 1: Create Superuser (Admin Account)

Run this command to create your admin account:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username (e.g., `admin`)
- Email address (optional)
- Password (enter twice)

**Example:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
```

## Step 2: Start the Development Server

```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

## Step 3: Access Django Admin

Open your browser and go to:
```
http://127.0.0.1:8000/admin/
```

Login with the superuser credentials you just created.

## Step 4: Add Sample Data

In the Django Admin panel:

### 1. Create an Instructor User
   - Go to **Users** → **Add User**
   - Username: `instructor1`
   - Password: (set password)
   - Role: **Instructor**
   - First name: John
   - Last name: Doe
   - Email: john@example.com
   - Save

### 2. Create Instructor Profile
   - Go to **Instructor Profiles** → **Add**
   - User: Select `instructor1`
   - Employee ID: `INST-001`
   - Department: `Computer Science`
   - Save

### 3. Create a Student User
   - Go to **Users** → **Add User**
   - Username: `student1`
   - Password: (set password)
   - Role: **Student**
   - First name: Jane
   - Last name: Smith
   - Email: jane@example.com
   - Save

### 4. Create Student Profile
   - Go to **Student Profiles** → **Add**
   - User: Select `student1`
   - Student ID: `2024-001`
   - Year Level: **First Year**
   - Program: `BS Computer Science`
   - Save

### 5. Create a Course
   - Go to **Courses** → **Add**
   - Code: `BSCS`
   - Name: `Bachelor of Science in Computer Science`
   - Year Level: `1`
   - Description: `Computer Science Program`
   - Save

### 6. Create a Subject
   - Go to **Subjects** → **Add**
   - Code: `CS101`
   - Name: `Introduction to Programming`
   - Course: Select `BSCS`
   - Units: `3`
   - Semester: **First Semester**
   - Year Level: `1`
   - Instructor: Select `instructor1`
   - Save

### 7. Enroll Student
   - Go to **Enrollments** → **Add**
   - Student: Select `student1`
   - Subject: Select `CS101`
   - Status: **Enrolled**
   - Save

### 8. Add Grade
   - Go to **Grades** → **Add**
   - Enrollment: Select `student1 enrolled in CS101`
   - Prelim Grade: `85.00`
   - Midterm Grade: `90.00`
   - Final Grade: `92.00`
   - Leave weights as default (30%, 30%, 40%)
   - Save
   
   **Note**: Weighted average, letter grade, and grade point will be auto-calculated!

### 9. Create Announcement
   - Go to **Announcements** → **Add**
   - Title: `Welcome to the new semester!`
   - Content: `Classes start next week. Please check your schedules.`
   - Announcement Type: **System-wide**
   - Is Active: ✓ (checked)
   - Save

## Step 5: Verify Everything Works

### Check Grade Calculation
1. Go to **Grades** in admin
2. Click on the grade you just created
3. Verify that **Weighted Average** is calculated (should be ~89.50)
4. Verify **Letter Grade** (should be 1.75)
5. Verify **Grade Point** (should be 3.25)

### Check User Roles
1. Go to **Users**
2. Verify you see different users with their roles
3. Check that student and instructor profiles are linked

## 📊 Grade Calculation Example

For the sample grades entered:
- Prelim: 85.00 × 30% = 25.50
- Midterm: 90.00 × 30% = 27.00
- Final: 92.00 × 40% = 36.80
- **Weighted Average: 89.30**
- **Letter Grade: 1.75** (88-90 range)
- **Grade Point: 3.25**

## 🎯 What's Next?

Your backend is fully functional! You can now:

1. ✅ Manage users (students, instructors, admins)
2. ✅ Create courses and subjects
3. ✅ Enroll students
4. ✅ Enter and calculate grades
5. ✅ Post announcements
6. ✅ Track GPA

### Ready for Frontend?

Once you're comfortable with the backend, you can start building:
- Login/Registration pages
- Student dashboard (view grades, announcements)
- Instructor dashboard (enter grades, view rosters)
- Admin dashboard (manage everything)
- Grade portal interface
- Profile management pages

## 🔍 Useful Admin Commands

### View all users
```bash
python manage.py shell
>>> from accounts.models import User
>>> User.objects.all()
```

### Check Django version
```bash
python manage.py --version
```

### Run database migrations (if you make model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🐛 Troubleshooting

### Can't login to admin?
- Make sure you created a superuser
- Check if you're using the correct password
- Username is case-sensitive

### Images not uploading?
- Make sure `media/` folder exists
- Check file permissions
- Pillow must be installed (`pip install Pillow`)

### Grade not calculating?
- All three grades (prelim, midterm, final) must be entered
- Weights must sum to 100%
- Click "Save" to trigger calculation

---

**✨ Backend is ready! Have fun exploring the system!**
