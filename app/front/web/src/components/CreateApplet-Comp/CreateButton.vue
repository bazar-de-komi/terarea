<template>
  <button class="create-button" @click="createApplet">Create</button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  emits: ['create'],
  setup(_, { emit }) {
    const createApplet = () => {
      emit('create');
    };

    return { createApplet };
  },
});
</script>

<style scoped>
.create-button {
  background-color: #4CAF50;
  color: white;
  font-size: 24px;
  font-weight: bold;
  padding: 15px 40px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  margin-top: 40px;
  transition: 0.3s;
}

.create-button:hover {
  background-color: #45a049;
}
</style>
