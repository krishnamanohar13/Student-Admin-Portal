from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
import csv
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Manu123@localhost:3306/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}', '{self.mobile}', '{self.course}', '{self.payment_status}')"

# Route for the index page
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

# Route for the student registration form and form processing
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        course = request.form['course']
        payment_status = request.form['payment_status']

        # Create a new student record
        new_student = Student(name=name, email=email, mobile=mobile, course=course, payment_status=payment_status)
        db.session.add(new_student)
        db.session.commit()
        flash('Student registered successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('registration_form.html')

# Route to delete a student record
@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('index'))

# Route to edit a student record and form processing
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        # Update student details
        student.name = request.form['name']
        student.email = request.form['email']
        student.mobile = request.form['mobile']
        student.course = request.form['course']
        student.payment_status = request.form['payment_status']
        db.session.commit()
        flash('Student details updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

# Route to download student records as CSV
@app.route('/download_csv')
def download_csv():
    students = Student.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Email', 'Mobile', 'Course', 'Payment Status'])
    for student in students:
        writer.writerow([student.name, student.email, student.mobile, student.course, student.payment_status])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=students.csv'})

if __name__ == '__main__':
    app.run(debug=True)
