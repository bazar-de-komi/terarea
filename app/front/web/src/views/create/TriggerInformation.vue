<template>
  <div v-if="triggerDetails" :style="{ backgroundColor: triggerDetails.backgroundColor }" class="details-container">
    <h1>{{ triggerDetails.title }}</h1>
    <p>{{ triggerDetails.description }}</p>
    <p>Service: {{ triggerDetails.name }}</p>
  </div>
  <div v-else class="loading">Chargement...</div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { queries } from '../../../lib/querier';

export default defineComponent({
  setup() {
    const route = useRoute();
    const triggerDetails = ref<any>(null);

    const fetchTriggerDetails = async () => {
      try {
        const id = route.params.id;
        triggerDetails.value = await queries.get(`/triggers/${id}`);
      } catch (error) {
        console.error("Erreur lors de la récupération du trigger:", error);
      }
    };

    onMounted(fetchTriggerDetails);

    return {
      triggerDetails,
    };
  },
});
</script>

<style scoped>
.details-container {
  padding: 20px;
  color: white;
  text-align: center;
  border-radius: 10px;
}
.loading {
  text-align: center;
  font-size: 1.2rem;
}
</style>


<style scoped>
.trigger-tile {
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  position: relative;
  width: 250px;
  height: 300px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.trigger-tile:hover {
  transform: scale(1.05);
}

.trigger-title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
  margin-bottom: 15px;
  color: #fff;
  word-wrap: break-word;
  white-space: normal;
}

.trigger-description {
  margin-top: 10px;
  color: #333;
}

.trigger-tile-link {
  text-decoration: none;
  color: inherit;
}

.trigger-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 24px;
  height: 24px;
}
</style>
