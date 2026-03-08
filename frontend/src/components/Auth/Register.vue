<template>
    <div class="container-fluid min-vh-100 d-flex justify-content-center align-items-center bg-light">
        <div class="row w-100 justify-content-center">
            <div class="col-12 col-md-6 col-lg-4">
                <div class ="card bg-white shadow-sm">
                    <div class="card-body bg-white">
                        <h3 class ="card-title mb-5 text-primary">Register</h3>
                        <form @submit.prevent="register">
                            <div v-if="error" class="alert alert-danger">{{ error }}</div>
                            <div class="row mb-3 align-items-center">
                                <div class ="col-12 col-sm-3"><label for="name" class="form-label mb-0">Name</label></div>
                                <div class="col-12 col-sm-9"><input type="text" id="name" v-model="name" class="form-control" required></div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3">
                                    <label for="email" class="form-label mb-0">Email</label>
                                </div>
                                <div class="col-12 col-sm-9"> 
                                    <input type="email" id="email" v-model="email" class="form-control" required>
                                </div>
                            </div>
                            <div class="row mb-3 align-items-center">
                                <div class="col-12 col-sm-3">
                                    <label for="password" class="form-label mb-0">Password</label>
                                </div>
                                <div class="col-12 col-sm-9">
                                    <input type="password" v-model="password" class="form-control" required>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">Register</button>
                        </form>
                        <div class="mt-3">Already have an account? <a href="/login">Login here</a></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {name: "",email: "",password: "",error: null}
    },
    methods: {
        async register() {
            try {
                const response = await fetch("http://localhost:5000/auth/registration", {
                    method: "POST",
                    headers: {
                        "content-type": "application/json"
                    },
                    body: JSON.stringify({
                        name: this.name,
                        email: this.email,
                        password: this.password
                    })
                })
                if (response.ok) {
                    this.$router.push("/login");
                } else {
                    const error_data = await response.json();
                    this.error = error_data.message || "registration failed";
                }
            } catch (error) {
                this.error = error;
            }
        }
    }
}
</script>
