from flask import request,jsonify
from application.utils.decorators import role_required
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from application.model import User,Doctor,Specialization,Appointment,Treatment,DoctorAvailability
from application.database import db
from application.cache import cache
from . import admin_bp
from datetime import datetime


@admin_bp.route('/add_specialization',methods=['POST'])
@role_required('admin')
def add_specialization():
    data =request.get_json()
    name =data.get('name')
    description =data.get('description')
    if not name or not description:
        return jsonify({'message':"Some fields are missing"}),400
    existing = Specialization.query.filter_by(name=name).first()
    if existing:
        return jsonify({'message':'This field already exist'})
    new =Specialization(name =name,description =description)
    db.session.add(new)
    db.session.commit()
    return jsonify({'message':'specialization added successfully'}),201

     
@admin_bp.route('/specialization')
@role_required('admin')
def specialization():
    specializations = Specialization.query.all()
    result = []
    for s in specializations:
        result.append({
            "id": s.id,
            "name": s.name
        })
    return jsonify(result),200
    

@admin_bp.route('/add_doctor',methods=['POST'])
@role_required('admin')
def add_doctor():
    data =request.get_json()
    email =data.get('email')
    name =data.get('name')
    password =generate_password_hash(data.get('password'))
    role ="doctor"
    specialization_name=data.get('specialization_name')
    experience =data.get('experience')
    if not all([email, name,password,specialization_name,experience]):
        return jsonify({"message":"some fields are not filled"}),400
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message":"This doctor already exist"}),409
    specialization =Specialization.query.filter_by(name=specialization_name).first()
    if not specialization:
        return jsonify({'message':'specialization does not exist.Please create specialization first'}),404

    user =User(email=email,name=name,password=password,role=role)
    db.session.add(user)
    db.session.flush()

    doctor =Doctor(user_id=user.id,experience=experience,
                   specialization_id=specialization.id)
    db.session.add(doctor)
    db.session.commit()
    cache.delete("admin:registered_doctors")
    return jsonify({"message":"Doctor was added successfully"}),201



@admin_bp.route('/<int:user_id>/edit_doctor',methods =['PATCH'])
@role_required('admin')
def edit_doctor(user_id):
    user =User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message":"Doctor does not exist"}),404
    data = request.get_json()
    name = data.get('name')
    email =data.get('email')
    password =data.get('password')
    experience =data.get('experience')
    specialization_name =data.get('specialization_name')

    if email and email != user.email:
        existing =User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"message":"Email already exist"}),409
        user.email =email
    if name:
        user.name =name
    if password:
        user.password = generate_password_hash(password)
    if experience:
        user.doctor_profile.experience=experience
    if specialization_name:
        specialization =Specialization.query.filter_by(name=specialization_name).first()
        if not specialization:
            return jsonify({"message":"Specialization does not exist"})
        user.doctor_profile.specialization_id =specialization.id
    db.session.commit()
    cache.delete("admin:registered_doctors")
    return jsonify({"message":"Doctor updated successfully"})


@admin_bp.route('<int:user_id>/doctor_history')
@role_required('admin')
def doctor_history(user_id):
    user =User.query.filter_by(id =user_id,role='doctor').first()
    if not user:
        return jsonify({"message":"Doctor does not exist"}),404
    doctor_info = {
    "name" : user.name,
    "email" : user.email,
    "experience" : user.doctor_profile.experience,
    "specialization_name" : user.doctor_profile.specialization.name
    }
    treatment_list =[]
    for appointment in user.doctor_profile.appointments:
        appointment_id = appointment.treatment.appointment_id
        
        t = Treatment.query.filter_by(appointment_id=appointment_id).first()
        treatment_list.append({
            "diagnosis": t.diagnosis,
            "prescription":t.prescription,
            "test_result":t.test_results,
            "medicine": t.medicine,
            "patient_name": t.appointment.patient.name
        })
    return jsonify({"doctor_info": doctor_info, "treatments": treatment_list}),200

   



@admin_bp.route('<int:user_id>/patient_history')
@role_required('admin')
def patient_history(user_id):
    user =User.query.filter_by(id =user_id).first()
    name =user.name
    email =user.email
    info ={"name":name,"email":email}
    treatment_info =[]
    for appoint in user.patient_appointments:
        appointment_id = appoint.treatment.appointment_id
        t =Treatment.query.filter_by(appointment_id=appointment_id).first()
        treatment_info.append({
            "diagnosis": t.diagnosis,
            "prescription":t.prescription,
            "test_result":t.test_results,
            "medicine": t.medicine,
           
        })
    return jsonify({"info":info,"treatement_info":treatment_info}),200






@admin_bp.route('/<int:user_id>/block',methods=['PATCH'])
@role_required('admin')
def block_user(user_id):
    user =User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'User not found'}),404
    user.status ='blocked'
    db.session.commit()
    cache.delete("admin:registered_doctors")
    cache.delete("admin:registered_patients")
    return jsonify({'message':"User was blocked successfully"}),200



@admin_bp.route('/<int:user_id>/unblock',methods=['PATCH'])
@role_required('admin')
def unblock_user(user_id):
    user =User.query.filter_by(id = user_id).first()
    if not user:
        return jsonify({"message":"User not found"}),404
    user.status="active"
    db.session.commit()
    cache.delete("admin:registered_doctors")
    cache.delete("admin:registered_patients")
    return jsonify({"message":"User was unblocked successfully"}),200


@admin_bp.route('/<int:user_id>/delete',methods =['DELETE'])
@role_required('admin')
def delete_user(user_id):
    user =User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message":"User does not exist"}),404
    db.session.delete(user)
    db.session.commit()
    cache.delete("admin:registered_doctors")
    cache.delete("admin:registered_patients")
    return jsonify({"message":"User deleted successfully"}),200


@admin_bp.route('/registered_doctors')
@role_required('admin')
def registered_doctors():
    search = request.args.get("search", "").strip()
    if not search:
        cache_key = "admin:registered_doctors"
        cached = cache.get(cache_key)
        if cached is not None:
            return jsonify(cached), 200

    doctors_query = User.query.filter_by(role='doctor')
    if search:
        doctors_query = doctors_query.filter(User.name.ilike(f"%{search}%"))
    doctors = doctors_query.all()
    if not doctors:
        return jsonify({'No doctor is present right now'}),200
    doctor_list =[]
    for doctor in doctors:
        doctor_list.append({
        "name": doctor.name,
        "user_id": doctor.id,
        "experience": doctor.doctor_profile.experience,
        "specialization_id": doctor.doctor_profile.specialization_id,
        "specialization_name": doctor.doctor_profile.specialization.name,
        "status":doctor.status
        })
    if not search:
        cache.set(cache_key, doctor_list, timeout=60)
    return jsonify(doctor_list),200


@admin_bp.route('/registered_patients')
@role_required('admin')
def registered_patient():
    search = request.args.get("search", "").strip()
    if not search:
        cache_key = "admin:registered_patients"
        cached = cache.get(cache_key)
        if cached is not None:
            return jsonify(cached), 200

    patients_list =[]
    patients = User.query.filter_by(role='patient')
    if search:
        patients = patients.filter(User.name.ilike(f"%{search}%"))
    for patient in patients:
        patients_list.append({
            "name": patient.name,
            "id": patient.id,
            "email":patient.email,
            "status":patient.status

        })
    if not search:
        cache.set(cache_key, patients_list, timeout=60)
    return jsonify(patients_list),200




@admin_bp.route('/<int:user_id>/edit_patient',methods =['PATCH'])
@role_required('admin')
def edit_patient(user_id):
    user =User.query.filter_by(id = user_id).first()
    if not user:
        return jsonify({"message":"Patient does not exist"}),404
    data = request.get_json()
    name =data.get('name')
    email =data.get('email')
    password =data.get('password')

    if name:
        user.name = name
    if email and user.email != email:
        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"message":"Email already exist"}),409
        user.email =email
    if password:
        user.password =generate_password_hash(password)
    db.session.commit()
    cache.delete("admin:registered_patients")
    return jsonify({"message":"User was edited successfully"})


@admin_bp.route('/statistics')
@role_required('admin')
def statistics():
    patients = User.query.filter_by(role="patient").count()
    doctors = User.query.filter_by(role='doctor').count()
    appointments = Appointment.query.count()
    return jsonify({"patients":patients,"doctors":doctors,"appointments":appointments}),200


@admin_bp.route('/all_appointments')
@role_required('admin')
def appointments():
    cache_key = "admin:all_appointments"
    cached = cache.get(cache_key)
    if cached is not None:
        return jsonify(cached), 200

    appoints = Appointment.query.all()
    lists = []
    for appoint in appoints:
        lists.append({
            "id":appoint.id,
            "patient_id":appoint.patient_id,
            "doctor_id":appoint.doctor_id,
            "start_time": appoint.start_time.isoformat(),
            "end_time":appoint.end_time.isoformat(),
            "date":appoint.date.isoformat(),
            "status":appoint.status

        })
    cache.set(cache_key, lists, timeout=20)
    return jsonify(lists),200

@admin_bp.route('/<int:appoint_id>/cancel_appointment',methods =['PATCH'])
@role_required('admin')
def cancel_appointment(appoint_id):
    appointment = Appointment.query.filter_by(id = appoint_id).first()
    appointment.status ="cancelled"
    db.session.commit()
    cache.delete("admin:all_appointments")
    return jsonify({"message":"Appointment was cancelled"}),200


    



    
    
    


    
    
    



        




