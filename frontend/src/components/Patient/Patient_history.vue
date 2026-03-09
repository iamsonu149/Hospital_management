
<template>
    <Navbar :name="name"/>
    <div class="container-fluid" style="margin-top: 70px;">
        <div v-if="patient_history_error" class="alert alert-danger">
            {{ patient_history_error }}
        </div>
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="mb-0">Patient History</h3>
            <button class="btn btn-success" :disabled="isDownloading" @click="downloadCsvReport">
                {{ isDownloading ? "Preparing CSV..." : "Download CSV" }}
            </button>
        </div>
        <div v-if="download_message" class="alert alert-info">
            {{ download_message }}
        </div>
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
            name:localStorage.getItem("name"),
            isDownloading:false,
            download_message:""
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
        },
        async downloadCsvReport(){
            this.isDownloading = true;
            this.download_message = "Export started. Please wait...";

            try {
                const startResp = await axios.post(
                    `${this.base_api}/download_report`,
                    {},
                    { headers: this.authHeaders() }
                );
                const taskId = startResp.data.task_id;
                if (!taskId){
                    throw new Error("Task id not received");
                }

                const maxTries = 20;
                for (let i = 0; i < maxTries; i++) {
                    await new Promise(resolve => setTimeout(resolve, 1500));
                    const statusResp = await axios.get(
                        `${this.base_api}/download_report/status/${taskId}`,
                        { headers: this.authHeaders() }
                    );
                    const state = statusResp?.data?.state;

                    if (state === "SUCCESS") {
                        const fileName = statusResp?.data?.result?.file_name;
                        if (!fileName) {
                            throw new Error("CSV file name missing in task result");
                        }

                        const fileResp = await axios.get(
                            `${this.base_api}/download_report/file/${fileName}`,
                            { headers: this.authHeaders(), responseType: "blob" }
                        );

                        const url = window.URL.createObjectURL(new Blob([fileResp.data]));
                        const link = document.createElement("a");
                        link.href = url;
                        link.setAttribute("download", fileName);
                        document.body.appendChild(link);
                        link.click();
                        link.remove();
                        window.URL.revokeObjectURL(url);

                        this.download_message = "CSV downloaded successfully.";
                        this.isDownloading = false;
                        return;
                    }

                    if (state === "FAILURE") {
                        throw new Error(statusResp?.data?.message || "CSV export failed");
                    }
                }

                throw new Error("CSV export timed out. Try again.");
            } catch (error) {
                this.download_message = error?.response?.data?.message || error?.message || "Could not download CSV";
                this.isDownloading = false;
            }
        }
    }
}
</script>
