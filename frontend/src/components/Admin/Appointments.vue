<template>
    <div class="container-fluid mt-3">
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <h3>Upcoming Appointments</h3>
        <table class="table table-hover table-info w-100 admin-table">
            <thead>
                <tr>
                    <th>Patient Id</th>
                    <th>Doctor Id</th>
                    <th>Slot</th>
                    <th>Date</th>
                    <th class="text-end">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if ="appointments.length === 0">
                    <td colspan="5" class="p-0">
                        <div class="alert alert-info w-100 mb-0">
                            No appointments found.
                        </div>
                    </td>
                </tr>
                <tr v-for ="appointment in appointments" :key="appointment.id">
                    <td> {{ appointment.patient_id }}</td>
                    <td> {{ appointment.doctor_id }}</td>
                    <td> {{ Number(appointment.start_time.split(':')[0]) <12 ? '8:00 - 12:00' : '16:00 - 21:00'  }}</td>
                    <td> {{ appointment.date }}</td>
                    <td class="text-end text-nowrap">
                        <template v-if="appointment.status==='booked'">
                            <a class="btn btn-danger btn-sm" href="#" @click.prevent="$emit('cancel_appointment',appointment)">Cancel</a>
                        </template>
                        <span v-else-if="appointment.status==='cancelled'" class="text-danger">Cancelled</span>
                        <span v-else-if="appointment.status==='completed'" class="text-success">Completed</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

</template>

<script>
export default{
    name:"appointments",
    props:{
        error:{type:String,default:""},
        appointments:{type:Array,required:true}
    }
}

</script>

<style scoped>
.admin-table th,
.admin-table td {
    padding: 0.85rem 1.1rem;
}
</style>
