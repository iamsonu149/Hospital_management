from flask import request,jsonify
from application.utils.decorators import role_required
from application.model import User,Doctor,Specialization,Appointment,Treatment,DoctorAvailability
from . import patient_bp
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required,get_jwt_identity
from application.database import db
from datetime import datetime



@patient_bp.route('update_profile',methods =['POST'])
@role_required('patient')
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id =user_id).first()
    data =request.get_json()
    name =data.get('name')
    email =data.get('email')
    password =generate_password_hash(data.get('password'))
    user.name =name
    user.passoword =password
    user.email =email
    db.session.commit()
    return jsonify({"message":"Your profile was updated"}),200



@patient_bp.route('/specialization')
@role_required('patient')
def specialization():
    specializations = Specialization.query.all()
    result =[]
    for s in specializations:
        if s.doctors:
            result.append({"name":s.name,"id":s.id,"description":s.description},)
    return jsonify(result),200

@patient_bp.route('/<int:specialization_id>/doctors')
@role_required('patient')
def doctors(specialization_id):
    specialization = Specialization.query.filter_by(id= specialization_id).first()
    doctors = specialization.doctors
    doctors_list = []
    for doctor in doctors:
        doctors_list.append({"doctor_id":doctor.id,"specialization":specialization.name,
            "name":doctor.user.name,"experience":doctor.experience })
    return jsonify(doctors_list),200



@patient_bp.route('/<int:doctor_id>/available_slots')
@role_required('patient')
def available_slots(doctor_id):
    slots =DoctorAvailability.query.filter_by(doctor_id =doctor_id)
    slot_list =[]
    for slot in slots:
        slot_list.append({
        "slot_id" : slot.id,
        "doctor_id" : slot.doctor_id,
        "date" : slot.date.isoformat(),
        "start_time" : slot.start_time.isoformat(),
        "is_booked" : slot.is_booked })
    return jsonify(slot_list)

@patient_bp.route('/<int:slot_id>/book_slot',methods =['POST'])
@role_required('patient')
def book_slot(slot_id):
    slot = DoctorAvailability.query.get(slot_id)
    if not slot:
        return jsonify({"message": "slot not found"}), 200
    if slot.is_booked:
        return jsonify({"message":"slot already has been booked"}), 409
    slot.is_booked = True
    patient_id = get_jwt_identity()
    doctor_id = slot.doctor_id
    start_time = slot.start_time
    end_time = slot.end_time
    date = slot.date
    appointment = Appointment(patient_id=patient_id,doctor_id=doctor_id,
        start_time=start_time,end_time=end_time,date=date,availability_id=slot.id
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({ "message":"slot is booked successfully"}),201



@patient_bp.route('/patient_history')
@role_required('patient')
def patient_history():
    user_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(patient_id =user_id).all()
    if not appointments:
        return jsonify({"message":"No appointments found"}),200
    treatment =[]
    for appoint in appointments:
        treat = Treatment.query.filter_by(appointment_id=appoint.id).first()
        if treat:
            treatment.append({
                "treatment_id":treat.id,
                "test_result": treat.test_results,
                "medicine": treat.medicine,
                "diagnosis" : treat.diagnosis,
                "doctor_name":appoint.doctor.user.name

        })
    return jsonify(treatment),200


@patient_bp.route('/appointments')
@role_required('patient')
def appointments():
    user_id = get_jwt_identity()
    appoints = Appointment.query.filter_by(patient_id=user_id)
    info =[]
    for appoint in appoints:
        info.append({
            "patient_id":appoint.patient_id,
            "doctor_id":appoint.doctor_id,
            "start_time":appoint.start_time.isoformat(),
            "end_time":appoint.end_time.isoformat(),
            "date":appoint.date.isoformat(),
            "status":appoint.status
        })
    return jsonify(info),200

@patient_bp.route('<int:appoint_id>/cancel_appointment',methods =['PATCH'])
@role_required('patient')
def cancel_appointment(appoint_id):
    appointment = Appointment.query.filter_by(id = appoint_id).first()
    appointment.status ="cancelled"
    db.session.commit()
    return jsonify({"message":"Appointment was cancelled"}),200



   

