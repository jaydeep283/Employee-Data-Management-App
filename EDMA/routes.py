from EDMA import app, db
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from EDMA.models import Employee, User, Skill, Project, Team, Userskill, Userproject
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
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        doj = datetime.strptime(request.form['doj'], '%Y-%m-%d')
        years = request.form['years']
        # skills = request.form.getlist('skills')
        # projects = request.form['projects']
        #proj_list = projects.split(',')

        new_emp = Employee(emp_id=emp_id, name=name, user_type=user_type, dob=dob, doj=doj, years=years)
        db.session.add(new_emp)
        new_emp.user = current_user

        # exh_proj = []
        # for p in Project.query.all():
        #     exh_proj.append(p.name)
        # for proj in proj_list:
        #     pstrp = proj.strip()
        #     if pstrp in exh_proj:
        #         p = Project.query.filter_by(name=pstrp).first()
        #         current_user.projects.append(p)
        #     else:
        #         p = Project(name=pstrp)
        #         db.session.add(p)
        #         current_user.projects.append(p)

        # exh_skill = []
        # for s in Skill.query.all():
        #     exh_skill.append(s.name)
        # for skill in skills:
        #     if skill in exh_skill:
        #         s = Skill.query.filter_by(name=skill).first()
        #         current_user.skills.append(s)
        #     else:
        #         s = Skill(name=skill)
        #         db.session.add(s)
        #         current_user.skills.append(s)

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
        if emp is None:
            flash("Employee doesn't exist with Employee ID:{}!".format(id), category='danger')
            return render_template('delete.html')
        else:
            usr = emp.user
            tdel = Team.query.filter_by(emp_id=usr.details.emp_id).all()
            if len(tdel) == 0:
                pass
            else:
                for t in tdel:
                    db.session.delete(t)
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
        proj = request.form['searchProject']
        skill = request.form['searchSkill']
        level = request.form['seSkillLevel']
        lCheck = request.form.get('skillCheck')

        if id:
            lis = []
            emp_details = Employee.query.get(int(id))
            lis.append(emp_details)
            emp_det = lis[:]
            print(lis)
        elif name:
            emp_det = Employee.query.filter(Employee.name.like(str(name))).all()
            if len(emp_det) == 0:
                flash("Details not found related to {}! Try with valid name.".format(name), category='danger')
                return render_template('readMenu.html', load=firstLoad)
        elif proj:
            emp_det =[]
            p = Project.query.filter_by(name=proj).first()
            if p is None:
                flash("Details not found related to {}!".format(proj), category='danger')
                return render_template('readMenu.html', load=firstLoad)
            else:
                for usr in p.users:
                    emp_det.append(usr.details)
        elif skill and lCheck == '1':
            emp_det =[]
            s = Skill.query.filter_by(name=skill).first()
            if s is None or len(s.users) == 0:
                flash("Details not found related to Skill {}! Try again.".format(skill), category='danger')
                return render_template('readMenu.html', load=firstLoad)
            else:
                sid = s.id
                for usr in s.users:
                    uid = usr.id
                    if Userskill.query.filter_by(user_id=uid, skill_id=sid).first().rating >= int(level):
                        emp_det.append(usr.details)
                if len(emp_det) == 0:
                    flash("Details not found with requested Skill level or higher", category='danger')
                    return render_template('readMenu.html', load=firstLoad)
        elif skill:
            emp_det = []
            s = Skill.query.filter_by(name=skill).first()
            if s is None or len(s.users) == 0:
                flash("Details not found related to Skill {}! Try again.".format(skill), category='danger')
                return render_template('readMenu.html', load=firstLoad)
            else:
                for usr in s.users:
                    emp_det.append(usr.details)
        return render_template('readMenu.html', emp_det=emp_det, load=False)
    else:
        return render_template('readMenu.html', load=firstLoad)


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update_emp():
    if request.method == 'POST':
        id = request.form['emp_id']
        emp = Employee.query.get(id)
        # return redirect(url_for('update_emp_usr', id=id))
        return render_template('update.html', emp=emp)
    else:
        return render_template('updateAdm.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_emp_usr(id):
    emp = Employee.query.get(id)
    if request.method == 'POST':                           #and current_user.details.user_type == "Employee"
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
    # elif request.method == 'POST' and current_user.details.user_type == "Admin":
    #     return redirect(url_for('update_emp', emp=emp))
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


@app.route('/skills/<int:id>', methods=['GET', 'POST'])
def skills(id):
    emp = Employee.query.get(id)
    if request.method == 'POST':
        skill = request.form['skill']
        level = request.form['level']
        emp_exh_skills = [skill.name for skill in emp.user.skills]
        exh_skill = [s.name for s in Skill.query.all()]

        if skill in exh_skill:
            if skill in emp_exh_skills:
                uid = emp.user.id
                sid = Skill.query.filter_by(name=skill).first().id
                rating = Userskill.query.filter_by(user_id=uid, skill_id=sid).first().rating
                if level == rating:
                    flash("Skill already exists with same level!", category='danger')
                    return render_template('skill.html', id=id)
                else:
                    Userskill.query.filter_by(user_id=uid, skill_id=sid).first().rating = level
                    db.session.commit()
                    flash("Skill level updated!", category='success')
                    return render_template('skill.html', id=id)
            else:
                s = Skill.query.filter_by(name=skill).first()
                current_user.skills.append(s)
                db.session.commit()
                uid = emp.user.id
                sid = s.id
                Userskill.query.filter_by(user_id=uid, skill_id=sid).first().rating = level
                db.session.commit()
                flash("Skill added successfully!", category='success')
                return render_template('skill.html', id=id)
        else:
            s = Skill(name=skill)
            db.session.add(s)
            print(emp.user.username)
            emp.user.skills.append(s)
            db.session.commit()
            uid = emp.user.id
            print(uid)
            sid = s.id
            print(sid)
            print(Userskill.query.filter_by(user_id=uid, skill_id=sid).first().id)
            Userskill.query.filter_by(user_id=uid, skill_id=sid).first().rating = level
            db.session.commit()
            flash("Skill added successfully!", category='success')
            return render_template('skill.html', id=id)
    else:
        return render_template('skill.html', id=id)


@app.route('/teams', methods=['GET', 'POST'])
def addTeam():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        name = request.form['teamName']
        proj = request.form['projectName']
        designation = request.form['designation']
        emp = Employee.query.get(emp_id)
        t = Team(name=name, designation=designation, proj=proj)
        db.session.add(t)
        exh_proj = []
        for p in Project.query.all():
            exh_proj.append(p.name)

        if proj in exh_proj:
            p = Project.query.filter_by(name=proj).first()
            emp.user.projects.append(p)
            db.session.commit()
        else:
            p = Project(name=proj)
            db.session.add(p)
            emp.user.projects.append(p)
            db.session.commit()
        emp.team.append(t)
        db.session.commit()
        flash("Team details added successfully!", category='success')
        return render_template('addTeam.html')
    else:
        return render_template('addTeam.html')


@app.route('/teams/<int:emp_id>')
def viewTeam(emp_id):
    tlis = Team.query.filter_by(emp_id=emp_id).all()
    tnames = []
    for t in tlis:
        if not t.name in tnames:
            tnames.append(t.name)
    lis = []
    for tn in tnames:
        lis.extend(Team.query.filter_by(name=tn).all())
    if len(lis) == 0:
        flash("You don't have any Team Members", category='info')
        return redirect(url_for('index'))
    else:
        return render_template('viewTeam.html', tdet=lis, emp_id=emp_id)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out successfully!", category='info')
    return redirect(url_for('index'))
