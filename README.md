# CSE 108 Lab 8 – Student Enrollment Web App

## Live Demo
https://yeehawcuzzin.pythonanywhere.com

---

## Overview
This project is a full-stack web application built using Flask and SQLite that simulates a university enrollment system. It supports three roles: Student, Teacher, and Admin, each with different capabilities.

Passwords are securely hashed using Werkzeug before storage.

---

## Features

### Student
- View enrolled courses
- View all available courses
- Enroll in courses (with capacity limits)
- Drop courses

### Teacher
- View assigned courses
- View student rosters
- Edit student grades (with validation)

### Admin
- Full CRUD (Create, Read, Update, Delete) on:
  - Users
  - Courses
  - Enrollments
- Built using Flask-Admin
- Includes admin logout functionality

---

## Tech Stack
- Flask (backend)
- SQLite (database)
- Flask-Admin (admin interface)
- HTML/CSS (frontend)
- Werkzeug (password hashing)

---

## Demo Walkthrough Script

### Login View (20 pts)
Show:
- Login page loads

Do:
- Enter: `cnorris / pass`
- Click login

Say:
- Users authenticate through a login system with hashed passwords using Werkzeug.

---

### See all my classes (20 pts)
Show:
- Student dashboard → My Courses tab

Do:
- Point to enrolled courses list

Say:
- Students can view all currently enrolled courses.

---

### See all classes offered by school (20 pts)
Show:
- Click Available Courses tab

Do:
- Scroll if needed

Say:
- Students can view all available courses offered by the university.

---

### See number of students in my class (20 pts)
Show:
- Column like 5/10, 4/8

Say:
- Each course displays current enrollment versus capacity.

---

### Sign up for a new class (20 pts)
Do:
- Click + Add on a course

Show:
- Enrollment updates immediately

Say:
- Students can enroll in courses, and the system enforces capacity limits.

Optional:
- Attempt full class to show restriction

---

### Web App Design (20 pts)
Show:
- Clean UI (tabs, tables, buttons)

Say:
- The interface is structured with separate views and styled consistently for usability.

---

### Presentation Clarity (20 pts)
- Speak while clicking
- Maintain smooth flow
- Order: student → teacher → admin

---

## Admin Section (80 pts)

### Access Admin Panel
Do:
- Navigate to `/admin`

Say:
- Admin functionality is implemented using Flask-Admin.

---

### Create
Do:
- User → Create → add dummy user

Say:
- Admin can create new records such as users, courses, or enrollments.

---

### Read
Show:
- User table

Say:
- Admin can view all records in the database.

---

### Update
Do:
- Edit a record → Save

Show:
- “Record successfully saved”

Say:
- Admin can update existing records dynamically.

---

### Delete
Do:
- Delete a record

Say:
- Admin can delete records from the system.

---

### Multi-table CRUD
Do:
- Navigate between:
  - User
  - Course
  - Enrollment

Say:
- CRUD operations are supported across all database models.

---

### Admin Logout
Do:
- Click Logout in admin navbar

Say:
- Logout functionality was added directly into the admin interface.

---

## Teacher Functions (80 pts)

### Login as Teacher
Do:
- Login: `ahepworth / pass`

---

### See My Classes
Show:
- Teacher dashboard

Say:
- Teachers can view courses they are assigned to.

---

### See Students + Grades
Do:
- Click View Roster

Show:
- Student list with grades

Say:
- Teachers can view all enrolled students and their grades.

---

### Edit a Grade
Do:
- Modify grade → Save

Say:
- Grades are validated to ensure they are between 0 and 100.