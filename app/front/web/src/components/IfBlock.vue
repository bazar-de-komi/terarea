<template>
  <div :class="['if-block', serviceColor]">
    <!-- État du bouton "If" après sélection d'un service -->
    <div v-if="condition && condition.name">
      <img :src="condition.logo" alt="Service logo" class="service-logo" />
      <h3>{{ condition.name }}</h3>
      <p>{{ condition.description }}</p>

      <div class="actions">
        <!-- Bouton Edit -->
        <button @click="editService">Edit</button>
        <!-- Bouton Delete -->
        <button @click="deleteService">Delete</button>
      </div>
    </div>

    <!-- État initial du bouton avec "Add" -->
    <div v-else>
      <h3>If</h3>
      <p>Select a service...</p>
      <!-- Bouton Add -->
      <button @click="addService">Add</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    condition: {
      type: Object as PropType<{ name: string; description: string; logo: string; color: string } | null>,
      required: false
    }
  },
  computed: {
    // Détermine la couleur en fonction du service
    serviceColor(): string {
      return this.condition && this.condition.color ? this.condition.color : 'default-gray';
    }
  },
  methods: {
    // Simulation de la sélection d'un service
    addService() {
      this.$emit('service-selected', {
        name: 'Service XYZ',
        description: 'Every day at 8 AM',
        logo: '/path/to/logo.png',
        color: 'service-blue'
      });
    },
    // Édition du service sélectionné
    editService() {
      alert('Edit service');
    },
    // Suppression du service sélectionné
    deleteService() {
      this.$emit('service-selected', null); // Réinitialise le service
    }
  }
});
</script>

<style scoped>
.if-block {
  background-color: #ccc; /* Gris par défaut */
  color: black;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  position: relative;
  height: 120px; /* Ajustement de la hauteur */
  width: 300px; /* Ajustement de la largeur */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.service-logo {
  width: 30px;
  height: 30px;
  position: absolute;
  top: 10px;
  left: 10px;
}

.actions {
  display: flex;
  justify-content: center;
}

.actions button {
  margin-right: 10px;
  background-color: black;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.default-gray {
  background-color: #ccc;
}

.service-blue {
  background-color: #4a90e2;
}
</style>
