<template>
  <div class="row g-3 mb-3">
    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6 class="text-primary mb-1">Total Doctors</h6>
          <h3 class="mb-0">{{ stats.doctors }}</h3>
        </div>
      </div>
    </div>
    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6 class="text-primary mb-1">Total Patients</h6>
          <h3 class="mb-0">{{ stats.patients }}</h3>
        </div>
      </div>
    </div>
    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <h6 class="text-primary mb-1">Total Appointments</h6>
          <h3 class="mb-0">{{ stats.appointments }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StatsCards",
  props: {
    stats: {
      type: Object,
      required: true,
    },
  },
};
</script>
