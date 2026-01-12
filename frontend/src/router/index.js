import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from "../views/Dashboard.vue"
import UserForm from "../views/UserForm.vue"

const routes = [
    {path: '/', name: 'Dashboard', component: Dashboard},
    {path: '/novo-usuario', name: 'UserForm', component:UserForm}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router