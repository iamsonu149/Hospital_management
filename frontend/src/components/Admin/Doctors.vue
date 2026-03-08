<template>
    <div class="container-fluid mt-3">
        <div v-if="error" class="alert alert-danger">
            {{ error }}
        </div>
        <h3>Registered Doctors</h3>
        
        <table class = 'table table-hover table-info w-100 admin-table'>
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Experience</th>
                    <th>Specialization</th>
                    <th class="text-end">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="doctors.length === 0">
                    <td colspan="5" class="p-0">
                        <div class ="alert text-bg-info mb-0">
                            No doctors found.
                        </div>
                    </td>
                </tr>
                <tr v-for="doctor in doctors" :key="doctor.user_id">
                    <td>{{ doctor.user_id }}</td>
                    <td>{{ doctor.name }}</td>
                    <td>{{ doctor.experience }}</td>
                    <td>{{ doctor.specialization_name }}</td>
                    <td class="text-end text-nowrap">
                        <a class="btn btn-primary btn-sm" @click.prevent="$emit('edit-doctor', doctor)">Edit</a>
                        <span> | </span>
                        <a class="btn btn-danger btn-sm" href="#" @click.prevent="$emit('delete-doctor', doctor.user_id)">Delete</a>
                        <span> | </span>
                        <a class="btn btn-danger btn-sm" href="#" @click.prevent="$emit('toggle-block-doctor', doctor)">
                            {{ doctor.status === 'active' ? 'Block' : 'Unblock'  }}
                        </a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>


    <div v-if ="showEditModal" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog" style="margin-top: 20vh;">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Doctor</h5>
                    <button type="button" class="btn-close" @click="$emit('close-edit')"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="$emit('update-doctor', editForm)">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" id="name" v-model="editForm.name" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label for="experience" class="form-label">Experience</label>
                            <input type="text" id="experience" v-model="editForm.experience" class="form-control">
                        </div>
                        <div class="mb-3">
                            <label for="specialization" class="form-label">Specialization</label>
                            <select id="specialization" v-model="editForm.specialization_name" class="form-select" required>
                                <option disabled value="">Select Specialization</option>
                                <option v-for="s in specializations" :key="s.id" :value="s.name">{{ s.name }}</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Update Doctor</button>
                    </form> 
                </div>
            </div>
        </div>

    </div>

</template>

<script>

export default {
    name: "Doctors",
    props:{
        error:{type: String,default: ""},
        doctors:{type : Array,required:true},
        showEditModal: {type: Boolean,default: false},
        editForm:{type:Object, default: null},
        specializations:{type:Array,required:true}

    },
    emits: ["edit-doctor", "update-doctor", "delete-doctor", "toggle-block-doctor", "close-edit"]

}

</script>

<style scoped>
.admin-table th,
.admin-table td {
    padding: 0.85rem 1.1rem;
}
</style>
