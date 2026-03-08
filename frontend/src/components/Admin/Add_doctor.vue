<template>
    <Navbar :role="role" :name="adminName" />

    <div class="container-fluid min-vh-100 d-flex justify-content-center align-items-center bg-light"> 
        <div class="row w-100 justify-content-center">
            <div class="col-12 col-md-6 col-lg-4">
                <div class ="card bg-white shadow-sm">
                    <div class="card-body bg-white">
                        <h3 class ="card-title text-primary">Add Doctor</h3>
                        <form @submit.prevent="add_doctor">
                            <div v-if="error" class="alert alert-danger">{{ error }}</div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3"><label for="name" class="form-label">Name</label></div>
                                <div class="col-12 col-sm-9"> <input type="text" id="name" v-model="name" class="form-control" required></div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3"><label for="email" class="form-label">Email</label></div>
                                <div class="col-12 col-sm-9"> <input type="email" id="email" v-model="email" class="form-control" required></div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3"> <label for="password" class="form-label">Password</label></div>
                                <div class="col-12 col-sm-9"> <input type="password" id="password" v-model="password" class="form-control" required></div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3">
                                    <label for="specialization" class="form-label">Specialization</label>
                                </div>
                                <div class="col-12 col-sm-9">
                                    <select id="specialization" v-model="specialization_name" class="form-select" required>
                                        <option disabled value="">Select</option>
                                        <option v-for="s in specializations" :key="s.id" :value="s.name">{{ s.name }}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3"> <label for="exp" class="form-label">Experience</label></div>
                                <div class="col-12 col-sm-9"> <input type="text" id="exp" v-model="experience" class="form-control">  </div>
                            </div>
                            <button type="submit" class="btn btn-primary">Add Doctor</button>
                        </form>

                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import Navbar from "./Navbar.vue";
import axios from "axios";
export default{
    components: { Navbar },
    data(){
         return {role:"admin",adminName:"optimus",name:"",email:"",password:"",
            specialization_name:"",experience:"",error:"",specializations:[]}
    },
    mounted(){
        this.fetchSpecializations();
    },
    methods: {
        async fetchSpecializations(){
            const token = localStorage.getItem("token");
            try{
                const response = await axios.get("http://localhost:5000/admin/specialization", {
                    headers: { "Authorization": `Bearer ${token}` }
                });
                this.specializations = Array.isArray(response.data) ? response.data : [];
            }catch(error){
                this.error = error?.response?.data?.message || error?.response?.data?.msg || "Failed to load specializations.";
            }
        },
        async add_doctor(){
            const token = localStorage.getItem("token");
            if (!token){
                this.error = "Please login again.";
                this.$router.push("/login");
                return;
            }
            try{
                await axios.post("http://localhost:5000/admin/add_doctor",{
                    name:this.name,
                    email:this.email,
                    password: this.password,
                    specialization_name: this.specialization_name,
                    experience: this.experience
                }, {
                    headers: { "Authorization": `Bearer ${token}`}
                });
                this.error = "";
                this.$router.push("/admin/dashboard");
            }catch(error){
                this.error = error?.response?.data?.message || error?.response?.data?.msg || "Failed to add doctor.";
            }
        }

    }
}

</script>
