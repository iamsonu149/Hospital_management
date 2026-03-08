
<template>
    <Navbar :name="name"/>
    <div class="container-fluid" style="margin-top: 60px;">
        <div v-if="patient_history_error" class="alert alert-danger">
            {{ patient_history_error }}
        </div>
        <h3>Patient History</h3>
        <table class="table table-hover table-warning">
            <thead>
                <tr>
                    <th>Treatment Id</th>
                    <th>Doctor Name</th>
                    <th>Diagnosis</th>
                    <th>Test result</th>
                    <th>Medicine</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if ="patient_history.length === 0">
                    <td colspan="4" class="p-0">
                        <div class="alert text-bg-warning mb-0">
                            No history found
                        </div>
                    </td>
                    
                </tr>
                <tr v-for="treatment in patient_history" :key="treatment.treatment_id">
                    <td>{{ treatment.treatment_id }}</td>
                    <td>{{ treatment.doctor_name }}</td>
                    <td>{{ treatment.diagnosis }}</td>
                    <td>{{ treatment.test_result }}</td>
                    <td>{{ treatment.medicine }}</td>
                </tr>
            </tbody>
        </table>
    </div>

</template>

<script>
import axios from "axios";
import Navbar from "./Navbar.vue";
export default {
    components:{Navbar},
    data(){
        return {
            patient_history:[],
            patient_history_error:"",
            base_api:"http://localhost:5000/patient",
            name:localStorage.getItem("name")
        }
    },
    mounted(){
        this.fetch_patient_history();
    },
    methods:{
        authHeaders(){
            const token = localStorage.getItem("token");
            return { Authorization: `Bearer ${token}` };
        },
        async fetch_patient_history(){
            this.patient_history_error = "";
            try{
                const response= await axios.get(`${this.base_api}/patient_history`,{
                    headers:this.authHeaders()
                });
                this.patient_history = Array.isArray(response.data) ? response.data : [];
            } catch (error) {
                this.patient_history_error = error?.response?.data?.message || "Error fetching patient history";
            }
        }
    }
}
</script>
