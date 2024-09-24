<template>
  <button class="auth-button" @click="onClick">
    <img v-if="icon" :src="`/src/assets/${icon}.svg`" alt="icon" class="auth-icon" />
    {{ text }}
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    text: { type: String, required: true },
    icon: { type: String, required: false },
  },
  methods: {
    onClick() {
      console.log(`${this.text} clicked`);
    },
  },
});
</script>

<style scoped>
.auth-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 15px;
  margin-top: 10px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
}

.auth-icon {
  margin-right: 10px;
  height: 20px;
  width: 20px;
}
</style>
