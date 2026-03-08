<template>
    <nav class="navbar navbar-expand-sm bg-primary fixed-top">
        <div class="container-fluid">
            <div class="navbar-collapse show">
                <h2 class="text-dark">Hello, {{ name }}</h2>
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item ms-3">
                        <button class="btn btn-success" @click="create_slots">Create slots</button>
                    </li>
                    <li class="nav-item ms-3">
                        <button class="btn btn-danger" @click="logout">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

</template>

<script>
import axios from "axios";

export default {
    props: {
        role: {type: String,default: ""},
        name: {type: String,default: ""}
    },
    methods: {
        authHeaders(){
            const token = localStorage.getItem("token");
            return {
                Authorization: `Bearer ${token}`
            };
        },
        logout(){
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/login");
        },
       
        async create_slots(){
            try{
                await axios.post("http://localhost:5000/doctor/create_slots",{},{
                    headers:this.authHeaders()
                })
                alert("Slots created successfully for the next 7 days.")
            }catch(error){
                console.error("Error creating slots:", error);
                alert("Failed to create slots. Please try again.")
            }

        }

    }
}
</script>
