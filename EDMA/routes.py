from EDMA import app
from flask import render_template, request, redirect, url_for
from datetime import datetime
from EDMA.models import Employee


@app.route('/')
def index():
    return render_template('index.html')


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

        new_emp = Employee(emp_id=emp_id, name=name, user_type=user_type, dob=dob, doj=doj, years=years,
                           skill_set=skill_set, projects=projects)
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


@app.route('/update')
def update_emp():
    return render_template('update.html')