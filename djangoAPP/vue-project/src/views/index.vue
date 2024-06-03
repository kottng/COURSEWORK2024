<!-- <template>
    <navbar></navbar>
    <div class="plants">
        <h1>Hello user1! it is index</h1>
    </div>
</template>

<script setup>
import navbar from '../components/navbar.vue'
</script>

<style scoped>

</style> -->
<!-- <template>
    <div>
      <h1>Tasks</h1>
      <ul>
        <li v-for="task in tasks" :key="task.id">{{ task.id }}</li>
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
      axios.get('http://192.168.1.152:8800/api/Plants/')
        .then(response => {
          this.tasks = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
  };
  </script> -->

  <template>
    <div>
      <!-- Filters Card -->
      <div class="card mb-4 shadow" style="background-color: rgba(97, 172, 151, 1); border: none; border-radius: 5px; box-shadow: inset 0 0 15px rgb(255, 255, 255)">
        <div class="card-body" style="background-color: rgba(97, 172, 151, 1); border: none; border-radius: 5px; box-shadow: inset 0 0 15px rgb(255, 255, 255)">
          <h5 class="card-title">Filters</h5>
          
          <!-- Date Range Picker -->
          <div class="row mb-3">
            <div class="col-md-6">
              <label for="startDate" class="form-label">Start Date:</label>
              <input type="date" class="form-control" id="startDate" v-model="startDate">
            </div>
            <div class="col-md-6">
              <label for="endDate" class="form-label">End Date:</label>
              <input type="date" class="form-control" id="endDate" v-model="endDate">
            </div>
          </div>
  
          <!-- Dropdown for Plant Varieties -->
          <div class="row mb-3">
            <div class="col-md-12">
              <label for="variety" class="form-label">Plant Variety:</label>
              <select class="form-select" id="variety" v-model="selectedVariety">
                <option selected>Select Variety</option>
                <option v-for="variety in plantVarieties" :key="variety" :value="variety">{{ variety }}</option>
              </select>
            </div>
          </div>
  
          <!-- Apply Filters Button -->
          <div class="row mb-3">
            <div class="col-md-12">
              <button type="button" class="btn btn-outline-light" @click="applyFilters">Применить фильтры</button>
            </div>
          </div>
  
        </div>
      </div>
  
      <!-- Plants -->
      <div class="row mb-4 justify-content-center" v-for="plant in plants" :key="plant.id">
        <div class="col-md-8">
          <div class="card shadow" style="background-color: rgba(97, 172, 151, 1); border: none; border-radius: 5px; box-shadow: inset 0 0 15px rgb(255, 255, 255)">
            <div class="card-body" style="background-color: rgba(97, 172, 151, 1); border: none; border-radius: 5px; box-shadow: inset 0 0 15px rgb(255, 255, 255); color: white;">
              <h5 class="card-title">{{ plant.variety }}</h5>
              <p class="card-text">{{ plant.description }}</p>
              <p class="card-text" style="color: white;">ID: {{ plant.id }}</p>
              <router-link :to="'/viewPlant/' + plant.id" class="btn btn-outline-success">View Plant</router-link>
              <button @click="deletePlant(plant.id)" class="btn btn-outline-danger">Delete Plant</button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Add Plant Button -->
      <div class="row mt-4">
        <div class="col-md-12 d-flex justify-content-end">
          <div class="float-end">
            <router-link to="/addPlant" class="btn btn-success">Add Plant</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import 'bootstrap/dist/css/bootstrap.css';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        startDate: '',
        endDate: '',
        selectedVariety: 'Select Variety',
        plantVarieties: [],
        plants: []
      };
    },
    mounted() {
      // Fetch plant varieties
        this.fetchPlants();
        // axios.get('http://192.168.1.152:8000/api/Plants/')
        // .then(response => 
        // // {
        // //   this.tasks = response.data;
        // // }
        // console.log(response)
        // )
        // .catch(error => {
        //     console.error(error);
        // });
    },
    methods: {
      async fetchPlants() {
        try {
          const { response } = await axios.get('http://192.168.1.152:8000/api/Plants');
          this.plants = response.data;
          this.plantVarieties = [...new Set(response.data.map(plant => plant.variety))];
        } catch (error) {
          console.error('Error fetching plants:', error);
        }
      },
      applyFilters() {
        // Implement filter logic here
        // For example, filter by selected variety
        if (this.selectedVariety !== 'Select Variety') {
          this.plants = this.plants.filter(plant => plant.variety === this.selectedVariety);
        }
        // Additional filter logic for date range can be added here
      },
      async deletePlant(id) {
        // Implement delete logic here
        try {
          await axios.delete(`http://192.168.1.152:8800/api/Plants/${id}`);
          this.fetchPlants(); // Refresh the plant list after deletion
        } catch (error) {
          console.error('Error deleting plant:', error);
        }
      }
    }
  };
  </script>
  
  <style>
    body {
      background: rgb(33,122,103);
      background: linear-gradient(90deg, rgba(33,122,103,1) 63%, rgba(52,152,109,1) 100%);
    }
  </style>
    