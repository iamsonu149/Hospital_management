<template>
    <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center auth-bg">
        <div class="auth-overlay"></div>
        <div class="container position-relative">
            <div class="brand-copy text-dark d-none d-lg-block">
                <h1 class="fw-bold mb-2 ">Hospital Management</h1>
                <p class="mb-0">Secure appointments, reminders, and reports in one place.</p>
            </div>
            <div class="row justify-content-center justify-content-lg-end">
                <div class="col-12 col-md-10 col-lg-6 col-xl-5">
                    <div class="card border-0 shadow-lg">
                        <div class="card-body p-4 p-md-5">
                            <h3 class="card-title mb-4 text-primary">Login</h3>
                            <form @submit.prevent="login">
                                <div v-if="error" class="alert alert-danger">{{ error }}</div>
                                <div class="row mb-3 align-items-center">
                                    <div class="col-12 col-sm-3">
                                        <label for="email" class="form-label mb-0">Email</label>
                                    </div>
                                    <div class="col-12 col-sm-9">
                                        <input type="email" id="email" v-model="email" class="form-control" required />
                                    </div>
                                </div>
                                <div class="row mb-4 align-items-center">
                                    <div class="col-12 col-sm-3">
                                        <label for="password" class="form-label mb-0">Password</label>
                                    </div>
                                    <div class="col-12 col-sm-9">
                                        <input type="password" id="password" v-model="password" class="form-control" required />
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary">Login</button>
                                <div class="mt-3">Don't have an account? <a href="/register">Register here</a></div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default{
    data() {
        return {
            email: "",
            password: "",
            error:null
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post("http://localhost:5000/auth/login", {
                    email: this.email,
                    password: this.password
                });
                if (response.status === 200) {
                    const token = response.data.token;
                    localStorage.setItem("token",token);
                    localStorage.setItem("role",response.data.role);
                    localStorage.setItem("name",response.data.name)
                };
                const role = response.data.role;
                if (role === "admin"){
                    this.$router.push("/admin/dashboard");
                }else if ( role==="patient"){
                    this.$router.push("/patient/dashboard");
                }else{
                    this.$router.push("/doctor/dashboard");
                }
                    
                } catch (error){
                    this.error = error?.response?.data?.message || error?.message || "login failed";
                }
            }
        }
         
};

</script>

<style scoped>
.auth-bg {
    position: relative;
    min-height: 100vh;
    background-image:  url("https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
}


</style>
