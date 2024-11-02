<template>
  <div class="ifThisContainer">
    <div class="ifThisBlock">
      <span>If This</span>
      <button v-if="!serviceSelected" class="add-button" @click="addService">Add</button>
      <span v-else>{{ serviceSelected }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    serviceSelected: {
      type: String,
      default: '',
    },
  },
  emits: ['add-service'],
  methods: {
    addService() {
      this.$emit('add-service');
    }
  }
});
</script>

<style scoped>
.ifThisContainer {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Arial, sans-serif;
  padding: 10px;
  min-height: 30vh;
  box-sizing: border-box;
}

.ifThisBlock {
  background-color: black;
  color: white;
  padding: 10px 6vw;
  border-radius: 75px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 5vw;
  max-width: 90%;
  flex-wrap: wrap;
}

.ifThisBlock span {
  font-weight: bold;
  font-size: 5vw;
  white-space: nowrap;
}

.add-button {
  background-color: white;
  color: black;
  border-radius: 20px;
  padding: 1vw 1vw;
  font-size: 20px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  margin-left: 2vw;
}
</style>
