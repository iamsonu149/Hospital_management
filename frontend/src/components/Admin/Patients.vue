<template>
    <div class="container-fluid mt-3">
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <h3>Registered_patients</h3>
        <table class="table table-hover table-warning w-100 admin-table">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th class="text-end">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="patients.length===0">
                    <td colspan="4" class="p-0">
                        <div class="alert alert-info w-100 mb-0">
                            No patient found
                        </div>
                    </td>
                </tr>
                <tr v-for="patient in patients" :key="patient.id">
                    <td>{{ patient.id }}</td>
                    <td>{{ patient.name }}</td>
                    <td>{{ patient.email }}</td>
                    <td class="text-end text-nowrap">
                        <a class="btn btn-primary btn-sm" href="#" @click.prevent="$emit('edit_patient',patient)">Edit</a>
                        <span> | </span>
                        <a class="btn btn-danger btn-sm" href="#" @click.prevent="$emit('delete_patient',patient.id)">Delete</a>
                        <span> | </span>
                        <a class="btn btn-danger btn-sm" href="#" @click.prevent="$emit('block_patient',patient)">
                            {{ patient.status==='active' ? 'Block' : 'Unblock'  }}
                        </a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div v-if="show_patient_edit" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title">Edit Patient</h5>
                <button type="button" class="btn-close" @click="$emit('close_patient_edit')"></button>
                </div>
            
                <div class="modal-body">
                    <form @submit.prevent="$emit('update_patient',patient_form)">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" id = "name" class="form-control" v-model="patient_form.name" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" id="email" class="form-control" v-model="patient_form.email" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Update Patient</button>

                    </form>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default{
    props:{
        error:{type:String ,default:""},
        patients:{type:Array,required:true},
        show_patient_edit:{type:Boolean,default:false},
        patient_form:{type:Object,default:null}
    }
}

</script>

<style scoped>
.admin-table th,
.admin-table td {
    padding: 0.85rem 1.1rem;
}
</style>
