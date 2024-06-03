import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const cors = require('cors');
const app = createApp(App);
app.use(router);
app.use(cors());
app.mount('#app');


