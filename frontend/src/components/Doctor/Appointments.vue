<template>
    <div class="container-fluid" style="margin-top: 60px;">
        <div v-if="appointment_error" class="alert alert-danger">{{ appointment_error }}</div>
        <h3>Upcoming Appointments</h3>
        <table class="table table-hover table-info w-100 dashboard-table">
            <thead>
                <tr>
                    <th>Patient Id</th>
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
                    
                    <td> {{ Number(appointment.start_time.split(':')[0]) <12 ? '8:00 - 12:00' : '16:00 - 21:00'  }}</td>
                    <td> {{ appointment.date }}</td>

                    <td class="text-end text-nowrap">
                        <template v-if="appointment.status==='booked'">
                            <a class="btn btn-primary btn-sm" href="#" @click.prevent="$emit('mark_as_complete',appointment)">Mark as complete</a>
                            <span> | </span>
                            <a class="btn btn-danger btn-sm" href="#" @click.prevent="$emit('cancel_appointment',appointment)">Cancel</a>
                        </template>
                        <a v-else-if="appointment.status==='completed'" class="btn btn-primary btn-sm" href="#" @click.prevent="$emit('edit_treatment',appointment.id)">Edit</a>
                        <span v-else-if="appointment.status==='cancelled'" class="text-danger">Cancelled</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>


    <div v-if="show_treatment" class="modal fade show d-block" tabindex="-1"> 
        <div class="modal-dialog" style="margin-top: 20vh;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Treatment Details</h5>
                    <button type="button" class="btn-close" @click="$emit('close_treatment')"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="$emit('save_treatment', treatment_form)">
                        <div class="mb-3">
                            <label for="diagnosis" class="form-label">Diagnosis</label>
                            <input type="text" id="diagnosis" v-model="treatment_form.diagnosis" class="form-control" required>

                        </div>
                        <div class="mb-3">
                            <label for="prescription" class="form-label">Prescription</label>
                            <input type="text" id="prescription" v-model="treatment_form.prescription" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label for="test_result" class="form-label">Test Result</label>
                             <input type="text" id="test_result" v-model="treatment_form.test_results" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label for="med" class="form-label">Medicine</label>
                            <input type="text" id="med" v-model="treatment_form.medicine" class="form-control" required>
                        </div>
                         <button type="submit" class="btn btn-primary">{{ is_edit_mode ? "Update" : "Save" }}</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default{
    name:"appointments",
    props:{
        appointment_error:{type:String,default:""},
        appointments:{type:Array,required:true},
        show_treatment:{type:Boolean,default:false},
        treatment_form:{type:Object,default:null},
        is_edit_mode:{type:Boolean,default:false}

    },
    emits: [
    "mark_as_complete",
    "edit_treatment",
    "cancel_appointment",
    "close_treatment",
    "save_treatment"
  ]
}

</script>

<style scoped>
.dashboard-table th,
.dashboard-table td {
    padding: 0.85rem 1.1rem;
}
</style>
