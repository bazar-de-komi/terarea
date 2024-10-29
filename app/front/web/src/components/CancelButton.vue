<template>
  <button @click="handleClick" class="cancel-button">
    Cancel
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'CancelButton',
  emits: ['cancel'],
  methods: {
    handleClick() {
      this.$emit('cancel');
    }
  }
});
</script>

<style scoped>
.cancel-button {
  background-color: white;
  border: 2px solid black;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  transition: background-color 0.3s, transform 0.2s ease;
  position: absolute;
  top: 120px;
  left: 40px;
}

.cancel-button:hover {
  background-color: #ddd;
  transform: scale(1.05);
}

.cancel-button:active {
  transform: scale(0.95);
}
</style>
