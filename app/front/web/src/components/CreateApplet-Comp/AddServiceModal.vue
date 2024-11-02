<template>
  <div class="modal-background" @click.self="closeModal">
    <div class="modal-content">
      <h2>Select a Service</h2>
      <ul>
        <li
          v-for="service in services"
          :key="service.id"
          @click="selectService(service)"
          class="service-item"
        >
          {{ service.name }}
        </li>
      </ul>
      <button class="close-button" @click="closeModal">Close</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  emits: ['select-service', 'close'],
  data() {
    return {
      services: [
        { id: 1, name: 'Email' },
        { id: 2, name: 'Slack' },
        { id: 3, name: 'Twitter' },
        { id: 4, name: 'Google Calendar' },
      ],
    };
  },
  methods: {
    selectService(service: any) {
      this.$emit('select-service', service);
    },
    closeModal() {
      this.$emit('close');
    },
  },
});
</script>

<style scoped>
.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 400px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

.service-item {
  padding: 10px;
  margin: 5px 0;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.service-item:hover {
  background-color: #ddd;
}

.close-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.close-button:hover {
  background-color: #0056b3;
}
</style>
