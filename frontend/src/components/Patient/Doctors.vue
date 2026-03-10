<template>
    <Navbar
    :name="name"
    :search_query="search_query_input"
    @update:search_query="search_query_input = $event"
    @run-search="run_search"
    />
    <div class="container-fluid" style="margin-top:90px;">
        <div v-if="doctor_error" class="alert alert-danger">{{ doctor_error }}</div>
        <table class="table table-hover table-danger w-100">
            <thead>
                <tr>
                    <th>Doctor Id</th>
                    <th>Name</th>
                    <th>Specialization</th>
                    <th>Experience</th>
                    <th>Action</th>
                </tr>
            </thead>
                <tbody>
                    <tr v-if="doctors.length === 0">
                        <td colspan="5" class="text-center">No doctor found</td>
                    </tr>
                    <tr v-for="doctor in doctors" :key="doctor.doctor_id">
                        <td>{{ doctor.doctor_id }}</td>
                        <td>{{ doctor.name }}</td>
                        <td>{{ doctor.specialization }}</td>
                        <td>{{ doctor.experience }}</td>
                        <td class="action-link">
                            <a class="btn btn-primary" href="#" @click.prevent="check_availability(doctor.doctor_id)">Check Availability</a>
                            <span> | </span>
                            <a class="btn btn-primary" href="#" @click.prevent="view_detail(doctor)">View Detail</a>
                        </td>
                    </tr>
                </tbody>
            
        </table>
    </div>


    <div v-if="show_availability" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Book slot</h5>
                    <button type="button" class="btn-close ms-auto" @click="close_booking()"></button>
                </div>
                <div class="modal-body">
                    <div v-if="availability_error" class="alert alert-danger">{{ availability_error }}</div>
                    <div v-if="booking_success" class="alert alert-success">{{ booking_success }}</div>
                    <table class="table table-hover table-primary">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Time</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="availability.length===0">
                                <td colspan="3" class="text-center">No slot found</td>
                            </tr>
                            <tr v-for="slot in availability" :key="slot.slot_id">
                                <td>{{ slot.date }}</td>
                                <td>
                                    <button type="button" class="btn w-100" :class="slot_btn_class(slot)" :disabled="slot.is_booked" @click="select_slot(slot)">
                                        {{ slot_label(slot.start_time) }}
                                    </button>
                                </td>
                                <td>
                                    <span :class="slot.is_booked ? 'text-danger' : 'text-success'">
                                        {{ slot.is_booked ? "Booked" : "Available" }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="d-flex justify-content-end">
                        <button type="button" class="btn btn-success" :disabled="!selected_slot" @click="book_slot()">Book</button>
                    </div>
                </div>
            </div>
        </div>
    </div>



    <div v-if="show_detail" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border border-2">
            <div class="modal-header">
                <h5 class="modal-title">Doctor Info</h5>
                <button type="button" class="btn-close" @click="close_detail()"></button>
            </div>
            <div class="modal-body p-4">
            <div class="row align-items-center">
                <div class="col-8">
                    <h4 class="mb-2">Dr. {{ selected_doctor.name }}</h4>
                    <p class="mb-1">{{ selected_doctor.specialization }}</p>
                    <p class="mb-3">{{ selected_doctor.experience }} Experience Overall</p>
                </div>
            </div>

            <p class="mt-2 mb-4">
                Dr. {{ selected_doctor.name }} is a {{ selected_doctor.specialization }} with {{ selected_doctor.experience }} of experience in this field.
            </p>

            
            </div>
        </div>
        </div>
  </div>
</template>

<script>
import axios from "axios"
import Navbar from "./Navbar.vue";

export default{
    components:{Navbar},
   data() {
    return {
        base_api: "http://localhost:5000/patient",
        doctor_error:"",
        doctors: [],
        name:localStorage.getItem('name') || "",
        show_availability:false,
        availability:[],
        availability_error:"",
        selected_slot:null,
        booking_success:"",
        selected_doctor:null,
        show_detail:false,
        search_query_input:""
    };

        },
   mounted(){
    this.fetch_doctors()
   },
   methods:{
    run_search(query){
        this.fetch_doctors(query || this.search_query_input);
    },
       authHeaders(){
           const token=localStorage.getItem('token');
           return {Authorization:`Bearer ${token}`};
       },
    async fetch_doctors(search = ""){
        try{
            const dept_id = this.$route.params.department_id
            const params = {};
            if ((search || "").trim()) {
                params.search = search.trim();
            }
            const response =await axios.get(`${this.base_api}/${dept_id}/doctors`,
                {headers: this.authHeaders(), params}
            )
            this.doctors =Array.isArray(response.data) ? response.data :[]
            
        }catch(error){
            this.doctor_error=error?.response?.data?.message 
        }
    },
    async check_availability(doctor_id){
        this.show_availability=true;
        this.availability_error="";
        this.booking_success="";
        this.selected_slot=null;
        try{
            const response=await axios.get(`${this.base_api}/${doctor_id}/available_slots`,
            {headers:this.authHeaders()});
            this.availability=Array.isArray(response.data) ? response.data : [];
        }catch(error){
            this.availability_error=error?.response?.data?.message || "failed to load availability";
        }
    },
    close_booking(){
        this.show_availability=false;
        
    },
    slot_label(start_time){
        if(start_time==="08:00:00"){ return "08:00 - 12:00"; }
        if(start_time==="16:00:00"){ return "16:00 - 21:00"; }
        return start_time;
    },
    slot_btn_class(slot){
        if(this.selected_slot && this.selected_slot===slot){ return "btn-primary"; }
        return slot.is_booked ? "btn-outline-danger" : "btn-outline-success";
    },
    select_slot(slot){
        if(slot.is_booked){ return; }
        this.selected_slot=slot;
    },
    async book_slot(){
        this.availability_error="";
        this.booking_success="";
        if(!this.selected_slot){ return; }
        if(!this.selected_slot.slot_id){ this.availability_error="slot id is missing from backend response"; return; }
        try{
            const response=await axios.post(`${this.base_api}/${this.selected_slot.slot_id}/book_slot`,{}, {headers:this.authHeaders()});
            this.booking_success=response?.data?.message || "slot booked successfully";
            await this.check_availability(this.selected_slot.doctor_id || this.$route.params.doctor_id);
            this.show_availability=false;
        }catch(error){
            this.availability_error=error?.response?.data?.message || "failed to book slot";
        }
    },
    async view_detail(doctor){
        this.selected_doctor = doctor;
        this.show_detail = true;
    },
    close_detail(){
        this.show_detail=false;
        this.selected_doctor=null;
    },

   }
}

</script>
