<template>
    <div class="container-fluid " style="padding-top:70px">
        <div v-if ="depart_error" class="alert alert-danger">{{ depart_error }}</div>
        <h3>Departments</h3>
        <table class="table table-hover table-warning dashboard-table">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th class="text-end">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="departments.length===0">
                    <td colspan="4" class="alert alert-info w-100">
                        No department found
                    </td>
                </tr>
                <tr v-for="depart in departments" :key="depart.id">
                    <td>{{ depart.id }}</td>
                    <td>{{ depart.name }}</td>
                    <td>{{ depart.description }}</td>
                    <td class="text-end">
                        <router-link class="btn btn-primary" :to="`/patient/dashboard/${depart.id}/doctors`">View Detail </router-link>
                    </td>
                </tr>
            </tbody>
        </table>

    </div>

</template>

<script>
export default{
    props:{
        depart_error:{type:String,default: ""},
        departments:{type:Array,required:true}
    }
}

</script>

<style scoped>
.dashboard-table th,
.dashboard-table td {
    padding: 0.85rem 1.1rem;
}
</style>
