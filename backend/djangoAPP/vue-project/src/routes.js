import Vue from 'vue'
import VueRouter from 'vue-router'
import Plants from './views/Plants.vue'

Vue.use(VueRouter)

export default new VueRouter ({
    mode:'history',
    base: process.env.BASE_URL,
    routes: [
        {
        path: '/',
        name: 'plants',
        copmonent: Plants,
        },
    ]
})
