from .database import db

class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    email =db.Column(db.String(100),unique=True,nullable=False)
    name =db.Column(db.String(100),nullable=False)
    password =db.Column(db.String(300),nullable=False)
    role =db.Column(db.String(20),nullable=False,default='patient')
    status =db.Column(db.String(20),default='active')


class Doctor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)
    specialization_id =db.Column(db.Integer,db.ForeignKey('specialization.id'),nullable=False)
    experience =db.Column(db.String(50),nullable=False)

    user=db.relationship('User',backref=db.backref('doctor_profile',uselist=False,cascade='all, delete-orphan'))



class Specialization(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.String(200),nullable=True)

    doctors =db.relationship('Doctor',backref='specialization',lazy=True)



class Appointment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    availability_id = db.Column(db.Integer,db.ForeignKey('doctor_availability.id'),nullable=False,unique=True)
    patient_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    doctor_id =db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=False)
    start_time =db.Column(db.Time, nullable=False)
    end_time =db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    status=db.Column(db.String(50),nullable=False,default='booked')

    patient =db.relationship('User',backref=db.backref('patient_appointments',cascade='all, delete-orphan'),foreign_keys=[patient_id])
    doctor =db.relationship('Doctor',backref=db.backref('appointments',cascade='all, delete-orphan'),foreign_keys=[doctor_id])
    treatment =db.relationship('Treatment',backref='appointment',uselist=False,cascade="all,delete-orphan")



class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id= db.Column(db.Integer, db.ForeignKey('appointment.id',ondelete='CASCADE'),nullable=False)
    diagnosis= db.Column(db.String(200), nullable=False)
    prescription=db.Column(db.String(200), nullable=False)
    test_results = db.Column(db.String(200), nullable=True)
    medicine =db.Column(db.String(200), nullable=True)


class DoctorAvailability(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date= db.Column(db.Date, nullable=False)
    start_time=db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_booked= db.Column(db.Boolean, default=False)
    doctor = db.relationship('Doctor',backref=db.backref('availabilities', cascade='all, delete-orphan'))



