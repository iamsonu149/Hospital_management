<template>
    <Navbar
    :name="name"
    />

    <Appointments
    :appointment_error="appointment_error"
    :appointments="appointments"
    :show_treatment="show_treatment"
    :treatment_form="treatment_form"
    :is_edit_mode="is_edit_mode"
    @mark_as_complete="mark_as_complete"
    @edit_treatment="edit_treatment"
    @cancel_appointment="cancel_appointment"
    @close_treatment="close_treatment"
    @save_treatment="save_treatment"
    />

    <Patients
    :patients="patients"
    :patient_error="patient_error"
    />
</template>


<script>
import axios from "axios"
import Navbar from "./Navbar.vue"
import Appointments from "./Appointments.vue";
import Patients from "./Patients.vue";

export default{
components:{Navbar,Appointments, Patients},
data(){
    return{
        "base_api":"http://localhost:5000/doctor",
        "name": localStorage.getItem("name"),
        "appointments":[],
        "appointment_error":"",
        "show_treatment": false,
        "treatment_form": null,
        "selected_appointment_id": null,
        "is_edit_mode": false,
        "patients":[],
        "patient_error":""
    }
},
mounted(){
    this.fetch_appointments();
    this.fetch_patients();
},
methods:{
    authHeaders(){
        const token =localStorage.getItem('token');
        return{
            "Authorization": `Bearer ${token}`
        }
    },
    async fetch_appointments(){
        try{
            const response = await axios.get(`${this.base_api}/appointments`,{
                headers:this.authHeaders()
            })
            this.appointments = response.data.appointment_list || response.data.appointments || [];
            this.appointment_error = "";

        }catch(error){
            this.appointment_error = error?.response?.data?.message
        }
    },
    async cancel_appointment(appointment){
        try{
              await axios.patch(`${this.base_api}/${appointment.id}/cancel_appointment`,{},{
                headers: this.authHeaders()
              })
              this.fetch_appointments();
        }catch(err){
            this.appointment_error = err?.response?.data?.message || "Failed to cancel appointment"
        }
    },
    async mark_as_complete(appointment){
        this.show_treatment = true;
        this.selected_appointment_id = appointment.id;
        this.is_edit_mode = false;
        this.treatment_form ={ diagnosis:"",prescription:"",test_results:"", medicine:"" }
    },
    async edit_treatment(appointment_id){
        try{
            const response = await axios.get(`${this.base_api}/${appointment_id}/treatment`,{
                headers: this.authHeaders()
            });
            this.selected_appointment_id = appointment_id;
            this.is_edit_mode = true;
            this.treatment_form = {
                diagnosis: response.data.diagnosis || "",
                prescription: response.data.prescription || "",
                test_results: response.data.test_results || "",
                medicine: response.data.medicine || ""
            };
            this.show_treatment = true;
        }catch(err){
            this.appointment_error = err?.response?.data?.message || "Failed to load treatment";
        }
    },
    async close_treatment(){
        this.show_treatment = false;
        this.treatment_form = null;
        this.selected_appointment_id = null;
        this.is_edit_mode = false;
    },
    async save_treatment(treatment_form){
        try{
            if (this.is_edit_mode){
                await axios.put(
                    `${this.base_api}/${this.selected_appointment_id}/treatment`,
                    treatment_form,
                    { headers: this.authHeaders() }
                );
            } else {
                await axios.post(
                    `${this.base_api}/${this.selected_appointment_id}/treatment`,
                    treatment_form,
                    { headers: this.authHeaders() }
                );
            }
            this.close_treatment();
            this.fetch_appointments();
        }catch(err){
            this.appointment_error = err?.response?.data?.message || "Failed to save treatment"
        }
    },
    async fetch_patients(){
        try{
            const response =await axios.get(`${this.base_api}/patients`,{
                headers:this.authHeaders()
            })
            this.patients= response.data.patients || [];
            this.patient_error ="";

        }catch(error){
            this.patient_error = error?.response?.data?.message || "Failed to load patients"
        }
    }
}

}


</script>


