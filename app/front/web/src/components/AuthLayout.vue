<template>
  <div class="auth-layout">
    <h1>{{ title }}</h1>
    <slot></slot>
    <router-link :to="linkPath" class="link">{{ linkText }}</router-link>
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
  max-width: 600px;
  margin: 75px auto;
  padding: 45px;
  text-align: center;
  background-color: #e0d8d7;
  border-radius: 30px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 30px;
  font-size: 42px;
  font-weight: bold;
}

.link {
  display: block;
  margin-top: 22.5px;
  color: black;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
