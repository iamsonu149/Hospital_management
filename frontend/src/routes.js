import {createWebHistory, createRouter} from "vue-router";
import Login from "./components/Auth/Login.vue";
import Register from "./components/Auth/Register.vue";
import Admin_Dashboard from "./components/Admin/Admin_Dashboard.vue";
import Add_doctor from "./components/Admin/Add_doctor.vue";
import Patient_dashboard from "./components/Patient/Patient_dashboard.vue";
import Doctors  from "./components/Patient/Doctors.vue"
import Patient_history from "./components/Patient/Patient_history.vue";
import Doctor_Dashboard from "./components/Doctor/Doctor_Dashboard.vue";
import Add_Specialization from "./components/Admin/Add_Specialization.vue";

const routes = [
    { path: "/", redirect: "/login" },
    { path :"/login", component:Login },
    { path: "/register", component:Register },
    {path: "/admin/dashboard",component:Admin_Dashboard},
    {path: "/admin/dashboard/add_doctor",component:Add_doctor},
    {path: "/admin/dashboard/add_specialization",component:Add_Specialization},
    {path:"/patient/dashboard",component:Patient_dashboard},
    {path:"/patient/dashboard/history",component:Patient_history},
    {path:"/patient/dashboard/:department_id/doctors",component:Doctors},
    {path:"/doctor/dashboard",component:Doctor_Dashboard}

]

const router =createRouter({
    history:createWebHistory(),
    routes
})
export default router;
