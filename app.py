from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    user_type = db.Column(db.String(15), nullable=False, default='Guest Employee')
    dob = db.Column(db.DateTime, nullable=False)
    doj = db.Column(db.DateTime, nullable=False)
    years = db.Column(db.Integer, nullable=False)
    skill_set = db.Column(db.String(125), nullable=False)
    projects = db.Column(db.String(125), nullable=False)

    def __repr__(self):
        return "Employee: " + str(self.emp_id)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     user_type = request.form['user_type']
#     name = request.form['emp_name']
#     if user_type == 'Admin':
#         return redirect(url_for('admin_wel', name=name))
#     else:
#         return redirect(url_for('guest_wel', name=name))
#
#
# @app.route('/admin/<name>')
# def admin_wel(name):
#     return render_template('admin.html', name=name)
#
#
# @app.route('/guest/<name>')
# def guest_wel(name):
#     return render_template('guest.html', name=name)


@app.route('/new_employee', methods=['GET', 'POST'])
def new_employee():
    added = False
    if request.method == 'POST':
        name = request.form['emp_name']
        emp_id = request.form['emp_id']
        user_type = request.form['user_type']
        # dob = request.form['dob']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        # doj = request.form['doj']
        doj = datetime.strptime(request.form['doj'], '%Y-%m-%d')
        years = request.form['years']
        skill_set = request.form['skill_set']
        projects = request.form['projects']

        new_emp = Employee(emp_id=emp_id, name=name, user_type=user_type, dob=dob, doj=doj, years=years, skill_set=skill_set, projects=projects)
        # try:
        db.session.add(new_emp)
        db.session.commit()
        added = True
        return render_template('index.html', is_added=added)
        # except:
        #     return 'There was a issue adding your task.'
        # return redirect('/')
    else:
        return render_template('new_empl.html')


@app.route('/delete')
def del_emp():
    return render_template('delete.html')


@app.route('/show_all')
def show_all():
    allEmp = Employee.query.order_by(Employee.emp_id)
    return render_template('read.html', AllEmp=allEmp)


@app.route('/readMenu', methods=['GET', 'POST'])
def readMenu():
    firstLoad = True
    if request.method == 'POST':
        id = request.form['searchID']
        name = request.form['searchName']
        if id:
            emp_det = Employee.query.get(int(id))
        elif name:
            emp_det = Employee.query.filter_by(name=str(name)).first()
        return render_template('readMenu.html', emp_det=emp_det, load=False)
    else:
        return render_template('readMenu.html', load=firstLoad)


@app.route('/update')
def update_emp():
    return render_template('update.html')


if __name__ == "__main__":
    app.run(debug=True)
