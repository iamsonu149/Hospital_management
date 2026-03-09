from celery import shared_task
import csv
import datetime
import os
from flask import current_app
from application.model import Appointment, User, Doctor
from jinja2 import Template
from datetime import date, timedelta
from application.mail import send_email
import requests

@shared_task(ignore_result=False, name="download_csv_report")
def csv_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    appointments = (Appointment.query.filter_by(patient_id=user_id, status='completed')
        .order_by(Appointment.date.desc()).all())

    base_dir = os.path.abspath(os.path.join(current_app.root_path, ".."))
    export_dir = os.path.join(base_dir, "static", "exports")
    os.makedirs(export_dir, exist_ok=True)
    file_name = f"treatment_{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    file_path = os.path.join(export_dir, file_name)

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "date", "doctor_name", "treatment_id", "test_results", "medicine", "diagnosis"
            
        ])

        for appt in appointments:
            treatment = appt.treatment  # from relationship
            writer.writerow([
                appt.date,
                appt.doctor.user.name,
                treatment.id,
                treatment.test_results,
                treatment.medicine,
                treatment.diagnosis    
                
            ])

    return {"file_name": file_name, "file_path": file_path}



@shared_task(ignore_result=False, name="monthly_activity_report")
def monthly_report():  
    today = date.today()
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    doctors = Doctor.query.all()

    for doctor in doctors:
        doctor_user = doctor.user
        if not doctor_user or not doctor_user.email:
            continue

        appointments = (
            Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status == "completed",
            Appointment.date >= first_day_prev_month,
            Appointment.date <= last_day_prev_month,
        ).order_by(Appointment.date.asc()).all()
        )


        rows = []
        for appt in appointments:
            t = appt.treatment
            rows.append({
                "date": appt.date,
                "patient_name": appt.patient.name if appt.patient else "",
                "diagnosis": t.diagnosis if t else "",
                "prescription": t.prescription if t else "",
                "medicine": t.medicine if t else "",
                "test_results": t.test_results if t else "",
            })

        mail_template = """
        <h3>Dear Dr. {{ doctor_name }},</h3>
        <p>Monthly treatment activity report ({{ month_label }})</p>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr>
                <th>Date</th>
                <th>Patient</th>
                <th>Diagnosis</th>
                <th>Prescription</th>
                <th>Medicine</th>
                <th>Test Results</th>
            </tr>
            {% for r in rows %}
            <tr>
                <td>{{ r.date }}</td>
                <td>{{ r.patient_name }}</td>
                <td>{{ r.diagnosis }}</td>
                <td>{{ r.prescription }}</td>
                <td>{{ r.medicine }}</td>
                <td>{{ r.test_results }}</td>
            </tr>
            {% endfor %}
        </table>
        <p>Total completed appointments: {{ rows|length }}</p>
        <p>Regards,<br>Hospital Management</p>
        """

        html = Template(mail_template).render(
            doctor_name=doctor_user.name,
            month_label=first_day_prev_month.strftime("%B %Y"),
            rows=rows
        )

        send_email(
            doctor_user.email,
            subject=f"Monthly Activity Report - {first_day_prev_month.strftime('%B %Y')}",
            message=html
        )

    return "Monthly reports sent"



WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAM3WFQSI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=3pMiUVsCbC-8xEMp4xOWr0c0Ukh0dFojGN3G-wLjkcA"

@shared_task(ignore_result=False, name="daily_appointment_reminder")
def daily_reminder():
    today = date.today()

    appointments = Appointment.query.filter(Appointment.date == today,Appointment.status == "booked" ).all()

    for appt in appointments:
        patient = appt.patient
        if not patient:
            continue

        doctor_name = appt.doctor.user.name if appt.doctor and appt.doctor.user else "your doctor"
        text = f"Hi {patient.name}, you have an appointment with Dr. {doctor_name} today at {appt.start_time}. Please visit the hospital on time."

        requests.post(WEBHOOK_URL, json={"text": text})

    return f"Reminders sent for {len(appointments)} appointments"
