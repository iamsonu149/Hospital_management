<template>
    <Navbar 
    :name="user_name"
    />

    <div class="container-fluid min-vh-100 d-flex justify-content-center align-items-center bg-light"> 
        <div class="row w-100 justify-content-center">
            <div class="col-12 col-md-6 col-lg-4">
                <div class ="card bg-white shadow-sm">
                    <div class="card-body bg-white">
                        <h3 class ="card-title text-primary">Add Specialization</h3>
                        <form @submit.prevent="add_specialization">
                            <div v-if="error" class="alert alert-danger">{{ error }}</div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3"><label for="name" class="form-label">Specialization Name</label></div>
                                <div class="col-12 col-sm-9"> <input type="text" id="name" v-model="specialization_name" class="form-control" required></div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3"><label for="description" class="form-label">Description</label></div>
                                <div class="col-12 col-sm-9"> <input type="text" id="description" v-model="description" class="form-control" required></div>
                            </div>
                            
                            
                            <button type="submit" class="btn btn-primary">Add Specialization</button>
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
         return {specialization_name:"", description:"", error:"",user_name:localStorage.getItem('name')}
    },
    methods: {
        async add_specialization(){
            const token = localStorage.getItem("token");
            if (!token){
                this.error = "Please login again.";
                this.$router.push("/login");
                return;
            }
            try{
                await axios.post(
                    "http://localhost:5000/admin/add_specialization",
                    {
                        name: this.specialization_name,
                        description: this.description
                    },
                    { headers: { "Authorization": `Bearer ${token}` }}
                );

                this.error = "";
                this.$router.push("/admin/dashboard");
            }catch(error){
                this.error = error?.response?.data?.message || "Failed to add specialization.";
            }
        }

    }
}

</script>
