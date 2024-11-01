<template>
  <header class="header">
    <!-- Logo avec lien vers la page d'accueil -->
    <router-link to="/" class="logo-link">
      <img src="@/assets/logo-white.png" alt="Logo" class="logo" />
    </router-link>
    <!-- Boutons de navigation -->
    <nav class="nav">
      <router-link to="/sign-in" class="nav-item">Log In</router-link>
      <router-link to="/sign-up" class="get-started-btn">Get Started</router-link>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AppHeaderMain',
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: inherit;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 25px;
  z-index: 1000;
  font-family: 'Arial', sans-serif;
  box-sizing: border-box;
}

.logo-link {
  display: flex;
  align-items: center;
}

.logo {
  width: 120px;
}

.nav {
  display: flex;
  align-items: center;
}

.nav-item {
  margin-right: 20px;
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 16px;
}

.get-started-btn {
  background-color: white;
  color: black;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 16px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.get-started-btn:hover {
  background-color: #999;
}
</style>
