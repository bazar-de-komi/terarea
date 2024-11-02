<template>
  <div class="thenThisContainer">
    <div class="ifThisBlock">
      <span>Then That</span>
      <button v-if="showAddButton && !serviceSelected" class="add-button" @click="addService">Add</button>
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
    showAddButton: {
      type: Boolean,
      default: false,
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
.thenThisContainer {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Arial, sans-serif;

  padding: 10px;
  min-height: 30vh;
  box-sizing: border-box;
}

.ifThisBlock {
  background-color: grey;
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

@media (max-width: 600px) {
  .ifThisBlock {
    padding: 8px 3vw;
    gap: 1vw;
  }

  .ifThisBlock span {
    font-size: 6vw;
  }
}
</style>
