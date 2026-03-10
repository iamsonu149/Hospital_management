
<template>
  <Navbar
    :role="role"
    :name="name"
    :search_query="search_query_input"
    :search_target="search_target_input"
    @update:search_query="search_query_input = $event"
    @update:search_target="search_target_input = $event"
    @run-search="run_search"
  />
  <div class="container-fluid" style="margin-top: 90px;">
    <StatsCards :stats="stats" />

    <Doctors
      :doctors="doctors"
      :specializations="specialization_name"
      :error="doctor_error"
      :editForm="editForm"
      :showEditModal="showEditModal"
      @edit-doctor="editDoctor"
      @update-doctor="updateDoctor"
      @close-edit="close_edit"
      @delete-doctor="deleteDoctor"
      @toggle-block-doctor="toggleBlockDoctor"
    />
  </div>

  <Patients
    :patients="patients"
    :error ="patient_error"
    :show_patient_edit="show_patient_edit"
    :patient_form="patient_form"
    @edit_patient="edit_patient"
    @close_patient_edit="close_patient_edit"
    @update_patient="update_patient"
    @delete_patient="delete_patient"
    @block_patient="block_patient"

  />
  <Appointments
  :error="appointment_error"
  :appointments="appointments"
  @cancel_appointment="cancel_appointment"
  />

</template>

<script>
import axios from "axios";
import Navbar from "./Navbar.vue";
import Doctors from "./Doctors.vue";
import Patients from "./Patients.vue";
import Appointments from "./Appointments.vue";
import StatsCards from "./StatsCards.vue";

export default {
  components: { Navbar, Doctors,Patients,Appointments,StatsCards },
  data() {
    return {
      base_api: "http://localhost:5000/admin",
      name: "optimus",
      role: "admin",
      doctors: [],
      doctor_error: "",
      editForm: { user_id: null, name: "", experience: "", specialization_name: "" },
      specialization_name: [],
      showEditModal: false,

      patients:[],
      patient_error:"",
      patient_form: {name:"",email:""},
      show_patient_edit:false,

      appointments:[],
      appointment_error:"",
      search_query_input:"",
      search_target_input:"doctor",
      stats: {
        doctors: 0,
        patients: 0,
        appointments: 0
      }
    };
  },
  mounted() {
    this.fetchDoctors();
    this.fetch_specialization();
    this.fetch_patients();
    this.fetch_appointments();
    this.fetch_statistics();
  },
  methods: {
    run_search(){
      const q = this.search_query_input.trim();
      if (this.search_target_input === "doctor") {
        this.fetchDoctors(q);
        this.fetch_patients("");
      } else {
        this.fetch_patients(q);
        this.fetchDoctors("");
      }
    },
    authHeaders() {
      const token = localStorage.getItem("token");
      return { Authorization: `Bearer ${token}` };
    },
    async fetch_statistics(){
      try{
        const response = await axios.get(`${this.base_api}/statistics`, {
          headers: this.authHeaders()
        });
        this.stats = {
          doctors: response?.data?.doctors ?? 0,
          patients: response?.data?.patients ?? 0,
          appointments: response?.data?.appointments ?? 0
        };
      }catch(err){
        this.stats = { doctors: 0, patients: 0, appointments: 0 };
      }
    },
    async fetchDoctors(search = "") {
      try {
        this.doctor_error = "";
        const params = {};
        if (search) {
          params.search = search;
        }
        const response = await axios.get(`${this.base_api}/registered_doctors`, {
          headers: this.authHeaders(),
          params,
        });
        this.doctors = Array.isArray(response.data) ? response.data : [];
      } catch (err) {
        this.doctor_error = err?.response?.data?.message ;
      }
    },
    async fetch_specialization(){
      try {
        const response = await axios.get(`${this.base_api}/specialization`, {
          headers: this.authHeaders()
        });
        this.specialization_name = Array.isArray(response.data) ? response.data : [];
      } catch (err) {
        this.doctor_error = err?.response?.data?.message || err?.response?.data?.msg || "Failed to load specializations.";
      }
    },
    async close_edit(){
      this.showEditModal=false
    },
    
    async editDoctor(doctor) {
      this.editForm ={ ...doctor };
      this.showEditModal=true;
    },

    async updateDoctor(doctor) {
      try {
        await axios.patch(
          `${this.base_api}/${doctor.user_id}/edit_doctor`,
          { ...doctor },
          { headers: this.authHeaders() }
        );
        await this.fetchDoctors();
        await this.fetch_statistics();
        this.showEditModal=false;
      } catch (err) {
        this.doctor_error = err?.response?.data?.message || "Failed to update doctor.";
      };


    },

    async deleteDoctor(userId) {
      if (!window.confirm("Delete this doctor?")) return;
      try {
        await axios.delete(`${this.base_api}/${userId}/delete`, {
          headers: this.authHeaders()
    
        });
        await this.fetchDoctors();
        await this.fetch_statistics();
      } catch (err) {
        this.doctor_error = err?.response?.data?.message || "Failed to delete doctor.";
      }
    },
    async toggleBlockDoctor(doctor) {
      const status =(doctor.status || "").toLowerCase();
      const endpoint =status === "blocked" ? "unblock" : "block";
      try {
        await axios.patch(
          `${this.base_api}/${doctor.user_id}/${endpoint}`,
          {},
          { headers: this.authHeaders() }
        );
        await this.fetchDoctors();
        await this.fetch_statistics();
      } catch (err) {
        this.doctor_error = err?.response?.data?.message || "Failed to update status.";
      }
    },
    async fetch_patients(search = ""){
      try{
      this.patient_error="";
      const params = {};
      if (search) {
        params.search = search;
      }
      const response = await axios.get(`${this.base_api}/registered_patients` ,{
        headers: this.authHeaders(),
        params
      });
      this.patients = Array.isArray(response.data) ? response.data : [];
      }catch(err){
        this.patient_error = err?.response?.data?.message 

      }
    },
    async delete_patient(user_id){
      if (!window.confirm("delete this patient?")) return;
      try{
        await axios.delete(`${this.base_api}/${user_id}/delete` ,{
          
          headers: this.authHeaders()
        });
        await this.fetch_patients();
        await this.fetch_statistics();

      }catch(err){
        this.patient_error =err?.response?.data?.message || "Failed to delete patient"

      }

    },
    async block_patient(patient){
      const endpoint = patient.status === "blocked" ? "unblock" :"block"
      try{
        await axios.patch(
          `${this.base_api}/${patient.id}/${endpoint}`,
          {},
          {headers:this.authHeaders()}
        );
        await this.fetch_patients();
        await this.fetch_statistics();

      }catch(err){
          this.error = err?.response?.data?.message || "Failed to block the patient"
      }
    },
    async close_patient_edit(){
      this.show_patient_edit=false
    },
    async edit_patient(patient){
      this.patient_form={...patient}
      this.show_patient_edit=true
    },
    async update_patient(patient){
      this.patient_error=""
      try{
        await axios.patch(`${this.base_api}/${patient.id}/edit_patient`,
          {...patient},
          {headers:this.authHeaders()}
        )
        this.fetch_patients();
        this.fetch_statistics();
        this.show_patient_edit=false
      }catch(err){
        this.patient_error=err?.response?.data?.message || "failed to edit doctor"

      }
    },
    async fetch_appointments(){
      try{
        this.appointment_error=""
        const response = await axios.get(`${this.base_api}/all_appointments`, {
          headers:this.authHeaders()
        })
        this.appointments = Array.isArray(response.data) ? response.data : [];
      }catch(err){
        this.appointment_error = err?.response?.data?.message ||"failed to load appointments"
      }
    },
    async cancel_appointment(appointment){
      this.appointment_error=""
      try{
        this.appointment_error="";
        await axios.patch(`${this.base_api}/${appointment.id}/cancel_appointment`,{},{
          headers: this.authHeaders()
        })
        this.fetch_appointments();
        this.fetch_statistics();
        
      }catch(err){
        this.appointment_error =err?.response?.data?.message || "Failed to cancel appointment"
      }
    }
  },
};
</script>
