<template>
    <nav class="navbar navbar-expand-sm bg-primary fixed-top">
        <div class="container-fluid">
            <div class="navbar-collapse show">
                <h2 class="text-light">Hello, {{ name }}</h2>
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item ms-3">
                        <router-link class="btn btn-success" to="/patient/dashboard">Home</router-link>
                    </li>
                    <li class="nav-item ms-3">
                        <button class="btn btn-success" @click="edit_profile">Edit profile</button>
                    </li>
                    <li class="nav-item ms-3">
                        <button class="btn btn-success" @click="show_history">Show History</button>
                    </li>
                    <li class="nav-item ms-3">
                        <button class="btn btn-danger" @click="logout">Logout</button>
                    </li>
                </ul>
                <form class="d-flex" @submit.prevent="run_search">
                    <input
                        class="form-control"
                        type="text"
                        placeholder="Search"
                        :value="local_search_query"
                        @input="update_search_query($event.target.value)"
                    >
                    <button class="btn btn-success ms-2" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>


    <div v-if="show_profile_edit" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title">Edit Profile</h5>
                <button type="button" class="btn-close" @click="close_profile_edit"></button>
                </div>

                <div class="modal-body">
                    <div v-if="profile_error" class="alert alert-danger">{{ profile_error }}</div>
                    <form @submit.prevent="update_profile">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" id="name" class="form-control" v-model="profile_form.name" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" id="email" class="form-control" v-model="profile_form.email">
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" id="password" class="form-control" v-model="profile_form.password">
                        </div>
                        <button type="submit" class="btn btn-primary">Update Profile</button>

                    </form>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import axios from "axios";

export default {
    props: {
        name: { type: String, default: "" },
        search_query: { type: String, default: "" }
    },
    emits: ["profile-updated", "update:search_query", "run-search"],
    data() {
        return {
            show_profile_edit: false,
            profile_form: {name: this.name , email: "",password: ""},
            profile_error: "",
            local_search_query: this.search_query
        }
    },
    watch: {
        search_query(new_value) {
            this.local_search_query = new_value || "";
        }
    },
    methods: {
        update_search_query(value) {
            this.local_search_query = value;
            this.$emit("update:search_query", value);
        },
        run_search() {
            this.$emit("run-search", this.local_search_query);
        },
        authHeaders() {
            const token = localStorage.getItem("token");
            return { Authorization: `Bearer ${token}` };
        },
        logout() {
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/login");
        },
        close_profile_edit() {
            this.profile_error = "";
            this.show_profile_edit = false;
        },
        async fetch_profile() {
            const response = await axios.get(
                "http://localhost:5000/patient/profile",
                { headers: this.authHeaders() }
            );
            return response.data;
        },
        async update_profile() {
            try {
                const payload = {
                    name: this.profile_form.name
                };

                if (this.profile_form.email) {
                    payload.email = this.profile_form.email;
                }
                if (this.profile_form.password) {
                    payload.password = this.profile_form.password;
                }

                await axios.patch(
                    "http://localhost:5000/patient/update_profile",
                    payload,
                    { headers: this.authHeaders() }
                );

                localStorage.setItem("name", this.profile_form.name);
                this.$emit("profile-updated", this.profile_form.name);
                this.close_profile_edit();
            } catch (error) {
                this.profile_error = error?.response?.data?.message || "Failed to update profile";
            }
        },
        async edit_profile() {
            this.profile_error = "";
            this.profile_form.name = this.name || "";
            this.profile_form.password = "";
            try{
                const profile = await this.fetch_profile();
                this.profile_form.email = profile?.email || "";
                this.profile_form.name = profile?.name || this.profile_form.name;
            }catch(error){
                this.profile_error = error?.response?.data?.message || "Failed to load profile";
            }
            this.show_profile_edit = true;
        },
        show_history() {
            this.$router.push("/patient/dashboard/history");
        }
    }
}
</script>
