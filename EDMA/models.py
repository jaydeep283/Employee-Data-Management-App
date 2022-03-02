from EDMA import db


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