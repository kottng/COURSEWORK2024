<!-- <script setup>
</script>

<template>
  <div id="app">
    <router-view />
  </div>
  
</template>

<style scoped>
</style> -->
<template>
  <div>
    <h1>Tasks</h1>
    <ul>
      <li v-for="task in tasks" :key="task.id">{{ task.description }}</li>
    </ul>
  </div>
  <router-view></router-view>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      tasks: [],
    };
  },
  mounted() {
    axios.get('http://192.168.1.152:8000/api/Plants/')
      .then(response => 
      // {
      //   this.tasks = response.data;
      // }
      console.log(response)
      )
      .catch(error => {
        console.error(error);
      });
  },
};
</script>