from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'acme-university-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enrollment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FLASK_ADMIN_SWATCH'] = 'flatly' # <-- make it look nice heheheehh

db = SQLAlchemy(app)
babel = Babel(app)

# ── Models ────────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student | teacher | admin

    enrollments = db.relationship('Enrollment', foreign_keys='Enrollment.student_id', backref='student', lazy=True)
    taught_courses = db.relationship('Course', backref='teacher', lazy=True)

    # Passwords are securely hashed using Werkzeug before being stored in the database
    def set_password(self, pw): self.password_hash = generate_password_hash(pw)

    # Verifies a plaintext password against the stored hashed password securely
    def check_password(self, pw): return check_password_hash(self.password_hash, pw)
    def __repr__(self): return self.full_name


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=10)

    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')

    @property
    def enrolled_count(self): return len(self.enrollments)
    @property
    # Determines if the course has reached its maximum enrollment capacity
    def is_full(self): return self.enrolled_count >= self.capacity
    def __repr__(self): return self.name


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=True)

    __table_args__ = (db.UniqueConstraint('student_id', 'course_id'),)
    def __repr__(self): return f'{self.student} / {self.course}'


# ── Flask-Admin ───────────────────────────────────────────────────────────────
class LogoutView(BaseView):
    def is_accessible(self):
        return session.get('role') == 'admin'

    @expose('/')
    def index(self):
        return redirect(url_for('logout'))

class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('role') == 'admin'
    def inaccessible_callback(self, name, **kwargs):
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))

admin = Admin(app, name='UCM Admin Dashboard')
admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Course, db.session))
admin.add_view(SecureModelView(Enrollment, db.session))
admin.add_view(LogoutView(name='Logout'))


# ── Seed Data ─────────────────────────────────────────────────────────────────

def seed():
    users = [
        ('cnorris',   'pass', 'Chuck Norris',      'student'),
        ('mnorris',   'pass', 'Mindy Norris',       'student'),
        ('jsantos',   'pass', 'Jose Santos',        'student'),
        ('bbrown',    'pass', 'Betty Brown',        'student'),
        ('jstuart',   'pass', 'John Stuart',        'student'),
        ('lcheng',    'pass', 'Li Cheng',           'student'),
        ('nlittle',   'pass', 'Nancy Little',       'student'),
        ('aranganath','pass', 'Aditya Ranganath',   'student'),
        ('ywchen',    'pass', 'Yi Wen Chen',        'student'),
        ('ahepworth', 'pass', 'Ammon Hepworth',     'teacher'),
        ('swalker',   'pass', 'Susan Walker',       'teacher'),
        ('rjenkins',  'pass', 'Ralph Jenkins',      'teacher'),
        ('admin',     'pass', 'Administrator',      'admin'),
    ]
    user_map = {}
    for uname, pw, name, role in users:
        u = User(username=uname, full_name=name, role=role)
        u.set_password(pw)
        db.session.add(u)
        user_map[uname] = u
    db.session.flush()

    courses_data = [
        ('Math 101',    'rjenkins',  'MWF 10:00-10:50 AM', 8),
        ('Physics 121', 'swalker',   'TR 11:00-11:50 AM',  10),
        ('CS 106',      'ahepworth', 'MWF 2:00-2:50 PM',   10),
        ('CS 162',      'ahepworth', 'TR 3:00-3:50 PM',    4),
    ]
    course_map = {}
    for name, teacher_uname, sched, cap in courses_data:
        c = Course(name=name, teacher=user_map[teacher_uname], schedule=sched, capacity=cap)
        db.session.add(c)
        course_map[name] = c
    db.session.flush()

    enrollments = [
        ('jsantos',    'Math 101',    92),
        ('bbrown',     'Math 101',    65),
        ('jstuart',    'Math 101',    86),
        ('lcheng',     'Math 101',    77),
        ('nlittle',    'Physics 121', 53),
        ('lcheng',     'Physics 121', 85),
        ('mnorris',    'Physics 121', 94),
        ('jstuart',    'Physics 121', 91),
        ('bbrown',     'Physics 121', 88),
        ('aranganath', 'CS 106',      93),
        ('ywchen',     'CS 106',      85),
        ('nlittle',    'CS 106',      57),
        ('mnorris',    'CS 106',      68),
        ('aranganath', 'CS 162',      99),
        ('nlittle',    'CS 162',      87),
        ('ywchen',     'CS 162',      92),
        ('jstuart',    'CS 162',      67),
    ]
    for uname, cname, grade in enrollments:
        db.session.add(Enrollment(student=user_map[uname], course=course_map[cname], grade=grade))
    db.session.commit()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def login():
    # Redirect already logged-in users to their respective dashboards
    if session.get('role'):
        return redirect(url_for(session['role'] + '_dashboard'))

    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if u and u.check_password(request.form['password']):
            session['user_id'] = u.id
            session['role'] = u.role
            session['full_name'] = u.full_name
            return redirect(url_for(u.role + '_dashboard'))
        flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/student')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    student = User.query.get(session['user_id'])
    enrolled_ids = {e.course_id for e in student.enrollments}
    all_courses = Course.query.all()
    return render_template('student.html', student=student, all_courses=all_courses, enrolled_ids=enrolled_ids)


@app.route('/student/enroll/<int:course_id>', methods=['POST'])
def enroll(course_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    course = Course.query.get_or_404(course_id)
    # Prevent enrollment if course is full or student is already enrolled
    if course.is_full:
        flash(f'{course.name} is full.', 'error')
    else:
        existing = Enrollment.query.filter_by(student_id=session['user_id'], course_id=course_id).first()
        if existing:
            flash('Already enrolled.', 'error')
        else:
            db.session.add(Enrollment(student_id=session['user_id'], course_id=course_id))
            db.session.commit()
            flash(f'Enrolled in {course.name}!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/student/drop/<int:course_id>', methods=['POST'])
def drop_course(course_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    # Look for the specific enrollment record
    enrollment = Enrollment.query.filter_by(student_id=session['user_id'], course_id=course_id).first()
    
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash('Successfully dropped the course.', 'success')
    else:
        flash('You are not enrolled in this course.', 'error')
        
    return redirect(url_for('student_dashboard'))

@app.route('/teacher')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))
    teacher = User.query.get(session['user_id'])
    return render_template('teacher.html', teacher=teacher)


@app.route('/teacher/course/<int:course_id>')
def course_roster(course_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('teacher_dashboard'))
    return render_template('roster.html', course=course)


@app.route('/teacher/grade/<int:enrollment_id>', methods=['POST'])
def update_grade(enrollment_id):
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))
    e = Enrollment.query.get_or_404(enrollment_id)
    if e.course.teacher_id != session['user_id']:
        flash('Access denied.', 'error')
        return redirect(url_for('teacher_dashboard'))
 
    grade = request.form.get('grade', type=int)

    # Validate grade input on the backend to ensure it is within the valid range (0–100)
    if grade is None or grade < 0 or grade > 100:
        flash('Grade must be between 0 and 100.', 'error')
    else:
        e.grade = grade
        db.session.commit()
        flash('Grade updated.', 'success')

    return redirect(url_for('course_roster', course_id=e.course_id))


@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return redirect('/admin')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        try:
            if not User.query.first():
                seed()
        except Exception as e:
            print("DB seed check failed:", e)

    app.run(debug=True)