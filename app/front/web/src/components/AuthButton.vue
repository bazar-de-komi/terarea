<template>
  <button class="auth-button" :style="{ backgroundColor: buttonColor, color: textColor }" @click="onClick" >
    <img v-if="icon" :src="icon" alt="icon" class="auth-icon" />
    <span>{{ text }}</span>
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    text: { type: String, required: true },
    icon: { type: String, required: false },
    buttonColor: { type: String, required: false, default: '#666' },
    textColor: { type: String, required: false, default: '#fff' },
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
  padding: 22.5px;
  margin-top: 15px;
  border: none;
  border-radius: 75px;
  font-size: 27px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s ease-in-out;
}

.auth-button:hover {
  background-color: #999;
}

.auth-button:active {
  background-color: #bbb;
  transform: scale(0.98);
}

.auth-icon {
  margin-right: 15px;
  height: 50px;
  width: 50px;
}
</style>
