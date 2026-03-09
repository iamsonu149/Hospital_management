import os
from flask import request,jsonify,send_from_directory,current_app
from application.utils.decorators import role_required
from application.model import User,Doctor,Specialization,Appointment,Treatment,DoctorAvailability
from . import patient_bp
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required,get_jwt_identity
from application.database import db
from celery.result import AsyncResult
from ..tasks import csv_report



@patient_bp.route('/update_profile',methods =['PATCH'])
@role_required('patient')
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id =user_id).first()
    if not user:
        return jsonify({"message":"User not found"}),404

    data =request.get_json()
    name =data.get('name')
    email =data.get('email')

    if name:
        user.name =name

    if email and email != user.email:
        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"message":"Email already exists"}),409
        user.email =email

    password = data.get('password')
    if password:
        user.password =generate_password_hash(password)

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


@patient_bp.route('/profile', methods=['GET'])
@role_required('patient')
def profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message":"User not found"}),404
    return jsonify({
        "name": user.name,
        "email": user.email
    }),200

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
            "id":appoint.id,
            "patient_id":appoint.patient_id,
            "doctor_id":appoint.doctor_id,
            "start_time":appoint.start_time.isoformat(),
            "end_time":appoint.end_time.isoformat(),
            "date":appoint.date.isoformat(),
            "status":appoint.status
        })
    return jsonify(info),200

@patient_bp.route('/<int:appoint_id>/cancel_appointment',methods =['PATCH'])
@role_required('patient')
def cancel_appointment(appoint_id):
    appointment = Appointment.query.filter_by(id = appoint_id).first()
    appointment.status ="cancelled"
    db.session.commit()
    return jsonify({"message":"Appointment was cancelled"}),200


@patient_bp.route('/download_report', methods=['POST'])
@role_required('patient')
def download_report():
    user_id = get_jwt_identity()
    task = csv_report.delay(user_id)
    return jsonify({"message": "CSV export started","task_id": task.id}), 202


@patient_bp.route('/download_report/status/<string:task_id>', methods=['GET'])
@role_required('patient')
def download_report_status(task_id):
    result = AsyncResult(task_id)

    if result.state == 'PENDING':
        return jsonify({"state": "PENDING", "message": "Task is queued"}), 200

    if result.state == 'FAILURE':
        return jsonify({"state": "FAILURE", "message": str(result.info)}), 500

    if result.state == 'SUCCESS':
        return jsonify({"state": "SUCCESS", "result": result.result}), 200

    return jsonify({"state": result.state}), 200


@patient_bp.route('/download_report/file/<string:file_name>', methods=['GET'])
@role_required('patient')
def download_report_file(file_name):
    base_dir = os.path.abspath(os.path.join(current_app.root_path, ".."))
    export_dir = os.path.join(base_dir, "static", "exports")
    file_path = os.path.join(export_dir, file_name)

    if not os.path.exists(file_path):
        return jsonify({"message": "File not found"}), 404

    return send_from_directory(export_dir, file_name, as_attachment=True)
