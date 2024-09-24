<template>
  <div class="auth-layout">
    <h1>{{ title }}</h1>
    <slot></slot>
    <router-link :to="linkPath">{{ linkText }}</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    title: { type: String, required: true },
    linkText: { type: String, required: true },
    linkPath: { type: String, required: true },
  },
});
</script>

<style scoped>
.auth-layout {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
}

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

.auth-button img {
  margin-right: 10px;
}

a {
  color: #000;
  display: block;
  margin-top: 15px;
}

.social-login {
  margin: 20px 0;
}
</style>
