<template>
    <Navbar
    :name="name"
    @profile-updated="name = $event"
    />
    
    <Departments
    :depart_error="depart_error"
    :departments="departments"
    />

    <Appointments
    :appointments="appointments"
    :appointment_error="appointment_error"
    @cancel_appointment="cancel_appointment"

    />
</template>

<script>
import Navbar from './Navbar.vue';
import axios from "axios"
import Departments from './Departments.vue';
import Appointments from './Appointments.vue';
export default{
    components: {Navbar,Departments,Appointments},
    data(){
        return {
            base_api: "http://localhost:5000/patient",
            name: localStorage.getItem('name') || "",
            depart_error :"",
            departments : [],
            appointments:[],
            appointment_error: ""
        }
    },
    mounted(){
        this.fetch_department();
        this.fetch_appointments();
    },
    methods:{
        authheader(){
            const token = localStorage.getItem('token');
            return {Authorization: `Bearer ${token}`};
        },
        async fetch_department(){
            this.depart_error=""
            try{
                const response = await axios.get(`${this.base_api}/specialization`,{
                    headers:this.authheader()
                });
                this.departments =Array.isArray(response.data) ? response.data :[]
            }catch(error){
                this.depart_error=error?.response?.data?.message 
            }
        },
        async fetch_appointments(){
            this.appointment_error=""
            try{
                const response = await axios.get(`${this.base_api}/appointments`,{
                    headers:this.authheader()
                });
                this.appointments=Array.isArray(response.data) ? response.data : []
            }catch(error){
                this.appointment_error =error?.response?.data?.message 
            }
        },
        async cancel_appointment(appointment){
            try{
                const appointId = appointment?.id || appointment?.appointment_id;
                if (!appointId){
                    this.appointment_error = "Appointment id is missing.";
                    return;
                }
                await axios.patch(
                    `${this.base_api}/${appointId}/cancel_appointment`,
                    {},
                    { headers:this.authheader() }
                );
                this.fetch_appointments();
            }catch(error){
                this.appointment_error =error?.response?.data?.message 
            }
        }
    }
}

</script>
