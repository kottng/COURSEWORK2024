import { createRouter, createWebHistory } from 'vue-router'
import index from './views/index.vue'
import About from './views/About.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name: "index", component: index},
        {path: '/about', name: "About", component: About}
    ]
})
export default router
