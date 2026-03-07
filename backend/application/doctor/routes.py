from flask import request,jsonify
from application.utils.decorators import role_required
from flask_jwt_extended import  get_jwt_identity
from application.model import User,Appointment,Treatment,DoctorAvailability
from application.database import db
from . import doctor_bp
from datetime import date, timedelta, time



@doctor_bp.route('/create_slots', methods=['POST'])
@role_required('doctor')
def create_slot():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.doctor_profile:
        return jsonify({"message": "Doctor not found"}), 404

    doctor_id = user.doctor_profile.id
    today = date.today()

    morning_start = time(8, 0)
    morning_end = time(12, 0)
    evening_start = time(16, 0)
    evening_end = time(21, 0)

    for offset in range(7):
        slot_date = today + timedelta(days=offset)

        existing_morning = DoctorAvailability.query.filter_by(doctor_id=doctor_id,
            date=slot_date,start_time=morning_start,end_time=morning_end).first()
        if not existing_morning:
            db.session.add(DoctorAvailability( doctor_id=doctor_id,date=slot_date,
                start_time=morning_start,end_time=morning_end,))

        existing_evening = DoctorAvailability.query.filter_by(doctor_id=doctor_id,
            date=slot_date,start_time=evening_start,end_time=evening_end).first()
        if not existing_evening:
            db.session.add(DoctorAvailability(doctor_id=doctor_id,date=slot_date,
                start_time=evening_start,end_time=evening_end,))

    db.session.commit()
    return jsonify({"message": "Availability created",}), 201


@doctor_bp.route('/slots', methods=['GET'])
@role_required('doctor')
def slots_of_next7days():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    doctor_id = user.doctor_profile.id
    today = date.today()
    end_date = today + timedelta(days=6)

    slots = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id, DoctorAvailability.date >= today,
        DoctorAvailability.date <= end_date).order_by(DoctorAvailability.date, DoctorAvailability.start_time).all()

    result = []
    for slot in slots:
        result.append({ "id": slot.id,"date": slot.date.isoformat(),
            "start_time": slot.start_time.strftime("%H:%M"),
            "end_time": slot.end_time.strftime("%H:%M"),
            "is_booked": slot.is_booked })

    return jsonify(result), 200



@doctor_bp.route('/<int:appointment_id>/treatment',methods =['POST'])
@role_required('doctor')
def treatment(appointment_id):
    appointment = Appointment.query.filter_by(id = appointment_id).first()
    if not appointment:
        return jsonify({"message":"Appointment not found"}),404
    if appointment.status =="completed":
        return jsonify({"message":"Appointment is already completed"}),409
    data = request.get_json()
    diagnosis = data.get('diagnosis')
    prescription = data.get('prescription')
    test_results = data.get('test_results')
    medicine = data.get('medicine')
    
    appointment.status = "completed"
    treatment = Treatment(appointment_id =appointment_id,diagnosis=diagnosis,
                          prescription=prescription,test_results=test_results,medicine=medicine)
    db.session.add(treatment)
    db.session.commit()
    return jsonify({"message":"Appointment is completed"}),201


@doctor_bp.route('/<int:appointment_id>/treatment', methods=['GET'])
@role_required('doctor')
def get_treatment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    if not appointment.treatment:
        return jsonify({"message": "Treatment not found"}), 404

    return jsonify({
        "appointment_id": appointment.id,
        "diagnosis": appointment.treatment.diagnosis,
        "prescription": appointment.treatment.prescription,
        "test_results": appointment.treatment.test_results,
        "medicine": appointment.treatment.medicine
    }), 200


@doctor_bp.route('/<int:appointment_id>/treatment',methods =['PUT'])
@role_required('doctor')
def update_treatment(appointment_id):
    treatment =Treatment.query.filter_by(appointment_id=appointment_id).first()
    if not treatment:
        return jsonify({"message":"Treatment not found"}),404

    data =request.get_json()
    diagnosis = data.get('diagnosis')
    prescription =data.get('prescription')
    test_results = data.get('test_results')
    medicine = data.get('medicine')

    treatment.diagnosis=diagnosis
    treatment.prescription = prescription
    treatment.test_results =test_results
    treatment.medicine =medicine
    db.session.commit()
    return jsonify({"message":"data was updated successfully"}),200


    
@doctor_bp.route('<int:appoint_id>/cancel_appointment',methods =['PATCH'])
@role_required('doctor')
def cancel_appointment(appoint_id):
    appointment = Appointment.query.filter_by(id = appoint_id).first()
    appointment.status ="cancelled"
    db.session.commit()
    return jsonify({"message":"Appointment was cancelled"})


@doctor_bp.route('/appointments')
@role_required('doctor')
def appointments():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id =user_id).first()
    appoints = user.doctor_profile.appointments
    appoints_list =[]
    for appoint in appoints:
        appoints_list.append({
            "id":appoint.id,
            "patient_id":appoint.patient_id,
            "start_time":appoint.start_time.isoformat(),
            "end_time":appoint.end_time.isoformat(),
            "date":appoint.date.isoformat(),
            "status":appoint.status
        })
    return jsonify({"appointment_list":appoints_list,"appointments":appoints_list}),200


@doctor_bp.route('/patients')
@role_required('doctor')
def patient_details():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user or not user.doctor_profile:
        return jsonify({"message":"Doctor not found"}),404

    doctor_id = user.doctor_profile.id
    appointments = Appointment.query.filter_by(doctor_id=doctor_id,status='booked').all()
    patients =[]
    seen =set()
    for appoint in appointments:
        patient = appoint.patient
        if patient.id not in seen:
            patients.append({
                "id":patient.id,
                "name":patient.name,
                "email":patient.email,
            })
            seen.add(patient.id)
    return jsonify({"patients":patients}),200
       
