<template>
     <div class="container-fluid mt-3">
        <div v-if="patient_error" class="alert alert-danger">{{ patient_error }}</div>
        <h3>Assigned Patients</h3>
        <table class="table table-hover table-info w-100 dashboard-table">
            <thead>
                <tr>
                    <th>Patient Id</th>
                    <th>Name</th>
                    <th>Email</th>
                 
                </tr>
            </thead>
            <tbody>
                <tr v-if ="patients.length === 0">
                    <td colspan="5" class="p-0">
                        <div class="alert alert-info w-100 mb-0">
                            No patients found.
                        </div>
                    </td>
                </tr>
                <tr v-for ="patient in patients" :key="patient.id">
                    <td> {{ patient.id }}</td>
                    <td> {{ patient.name }}</td>
                    <td> {{ patient.email }}</td>
                </tr>
            </tbody>
        </table>
    </div>

</template>

<script>
export default{
    props:{
        "patients":{type:Array, required:true},
        "patient_error":{type:String, required:true}
    }
}
</script>

<style scoped>
.dashboard-table th,
.dashboard-table td {
    padding: 0.85rem 1.1rem;
}
</style>
