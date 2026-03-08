<template>
    <nav class="navbar navbar-expand-sm bg-primary fixed-top">
        <div class="container-fluid">
            <div class="navbar-collapse show">
                <h2 class="text-dark">Hello, {{ name }}</h2>
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                     <li class="nav-item ms-3">
                        <button class="btn btn-success" @click="Home">Home</button>
                    </li>
                    <li class="nav-item ms-3">
                        <button class="btn btn-success" @click="add_doctor">Add Doctor</button>
                    </li>
                     <li class="nav-item ms-3">
                        <button class="btn btn-success" @click="add_specialization">Add Specialization</button>
                    </li>
                    <li class="nav-item ms-3">
                        <button class="btn btn-danger" @click="logout">Logout</button>
                    </li>
                </ul>
                <form class="d-flex" @submit.prevent="$emit('run-search')">
                    <select id="search-target" :value="search_target" @change="$emit('update:search_target', $event.target.value)" class="form-select">
                        <option value="doctor">Doctor</option>
                        <option value="patient">Patient</option>
                    </select>
                    <input class="form-control" type="text" placeholder="Search name" :value="search_query" @input="$emit('update:search_query', $event.target.value)">
                    <button class="btn btn-light ms-2" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>

</template>

<script>
export default {
    props: {
        role: { type: String, default: ""},
        name: {type: String,default: ""},
        search_query: { type: String, default: "" },
        search_target: { type: String, default: "doctor" }
    },
    emits:["update:search_query","update:search_target","run-search"],
    methods: {
        logout(){
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/login");
        },
        add_doctor(){
            this.$router.push("/admin/dashboard/add_doctor")
        },
        add_specialization(){
            this.$router.push("/admin/dashboard/add_specialization")
        },
        Home(){
            this.$router.push("/admin/dashboard")
        }






    }
}
</script>
