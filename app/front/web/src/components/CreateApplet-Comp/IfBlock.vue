<template>
  <div class="container">
    <div class="ifThisBlock">
      <span>If This</span>
      <button class="add-button" @click="addService">Add</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  methods: {
    addService() {
      alert('Add Service');
    }
  }
});
</script>

<style scoped>
.container {
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
  padding: 10px 5vw;
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
  margin-left : 2vw;
}

@media (max-width: 600px) {
  .ifThisBlock {
    padding: 8px 3vw;
    gap: 1vw;
  }

  .ifThisBlock span {
    font-size: 6vw;
  }

  .add-button {
    padding: 2vw 4vw;
    font-size: 4vw;
  }
}

</style>
