from EDMA import app, db
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from EDMA.models import Employee, User
from EDMA.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_employee', methods=['GET', 'POST'])
@login_required
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

        new_emp = Employee(emp_id=emp_id, name=name, user_type=user_type, dob=dob, doj=doj, years=years,
                           skill_set=skill_set, projects=projects)
        # try:
        db.session.add(new_emp)
        new_emp.user = current_user
        db.session.commit()
        added = True
        return render_template('index.html', is_added=added)
        # except:
        #     return 'There was a issue adding your task.'
        # return redirect('/')
    else:
        return render_template('new_empl.html')


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def del_emp():
    if request.method == 'POST':
        id = request.form['emp_id']
        emp = Employee.query.get(id)
        usr = emp.user
        db.session.delete(usr)
        db.session.delete(emp)
        db.session.commit()
        flash(f'Employee details deleted successfully!', category='success')
        return redirect(url_for('index'))
    else:
        if current_user.details.user_type == "Admin":
            return render_template('delete.html')
        else:
            flash(f'You do not have permission for this operation.', category='danger')
            return redirect(url_for('index'))


@app.route('/show_all')
@login_required
def show_all():
    allEmp = Employee.query.order_by(Employee.emp_id)
    return render_template('read.html', AllEmp=allEmp)


@app.route('/readMenu', methods=['GET', 'POST'])
@login_required
def readMenu():
    firstLoad = True
    if request.method == 'POST':
        id = request.form['searchID']
        name = request.form['searchName']
        if id:
            lis = []
            emp_details = Employee.query.get(int(id))
            lis.append(emp_details)
            emp_det = lis[:]
            print(lis)
        elif name:
            emp_det = Employee.query.filter(Employee.name.like(str(name)))
            print(emp_det)
        return render_template('readMenu.html', emp_det=emp_det, load=False)
    else:
        return render_template('readMenu.html', load=firstLoad)


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update_emp():
    if request.method == 'POST':
        id = request.form['emp_id']
        return redirect(url_for('update_emp_usr', id=id))
    else:
        return render_template('updateAdm.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_emp_usr(id):
    emp = Employee.query.get(id)
    if request.method == 'POST' and current_user.details.user_type == "Employee":
        emp.name = request.form['emp_name']
        emp.user_type = request.form['user_type']
        emp.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        emp.doj = datetime.strptime(request.form['doj'], '%Y-%m-%d')
        emp.years = request.form['years']
        emp.skill_set = request.form['skill_set']
        emp.projects = request.form['projects']
        db.session.commit()
        flash(f'Employee details updated successfully!', category='success')
        return redirect(url_for('index'))
    elif request.method == 'POST' and current_user.details.user_type == "Admin":
        return redirect(url_for('update_emp'))
    else:
        return render_template('update.html', emp=emp)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! Now you are logged in as {user_to_create.username}', category='success')
        return redirect(url_for('index'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error while creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('index'))
        else:
            flash(f"Username and password don't match! Please try again.", category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out successfully!", category='info')
    return redirect(url_for('index'))
