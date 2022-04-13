from EDMA import db
from EDMA import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_skill = db.Table('user_skill',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')))


user_project = db.Table('user_project',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('project_id', db.Integer, db.ForeignKey('project.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    skills = db.relationship('Skill', secondary=user_skill, backref='users')
    projects = db.relationship('Project', secondary=user_project, backref='users')

    def __repr__(self):
        return "<User: " + self.username + ">"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    user_type = db.Column(db.String(15), nullable=False, default='Employee')
    dob = db.Column(db.DateTime, nullable=False)
    doj = db.Column(db.DateTime, nullable=False)
    years = db.Column(db.Integer, nullable=False)
    # skill_set = db.Column(db.String(125), nullable=False)
    # projects = db.Column(db.String(125), nullable=False)
    user = db.relationship("User", backref='details', lazy='select', uselist=False)

    def __repr__(self):
        return "Employee: " + str(self.emp_id)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "Skill: " + str(self.id)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "Project: " + str(self.id)
