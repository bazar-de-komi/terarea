<template>
  <button class="cancel-button" @click="handleClick">
    Cancel
  </button>
</template>

<script lang="ts">
export default {
  methods: {
    handleClick() {
      this.$emit('cancel');
    }
  }
};
</script>

<style scoped>
.cancel-button {
  background-color: white;
  border: 2px solid black;
  color: black;
  font-weight: bold;
  border-radius: 20px;
  padding: 10px 20px;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.cancel-button:hover {
  background-color: transparent;
}

.cancel-button:active {
  transform: scale(0.98);
}

.cancel-button-container button {
  transition: background-color 0.3s, transform 0.2s ease;
}

.cancel-button-container button:hover {
  background-color: #ddd;
  transform: scale(1.05);
}

.cancel-button-container button:active {
  transform: scale(0.95);
}

</style>
