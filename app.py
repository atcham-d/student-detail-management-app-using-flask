from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecret'  # Required for flash messages

db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

@app.route('/')
def home():
    return redirect(url_for('index'))

# Route to display all students
@app.route('/students')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        new_student = Student(name=name, age=age)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Route to update a student's information
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('update_student.html', student=student)

# Route to delete a student
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    # Reset the auto-increment sequence for SQLite after deletion
    db.session.execute("DELETE FROM sqlite_sequence WHERE name='student'")

    db.session.commit()

    flash('Student deleted successfully!', 'danger')
    return redirect(url_for('index'))


# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
