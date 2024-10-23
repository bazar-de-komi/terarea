<template>
  <header class="header">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    <nav class="nav">
      <router-link to="/explore/all" class="nav-item">Explore</router-link>
      <router-link to="/create" class="nav-item create-btn">Create</router-link>
      <img src="@/assets/profile-icon.svg" alt="Profile" class="profile-icon" />
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: inherit;
  position: fixed;
  top: 0;
  left: 0;
  width: 98%;
  padding: 20px;
  z-index: 1000;
  font-family: 'Arial', sans-serif;
}

.logo {
  width: 100px;
}

.nav {
  display: flex;
  align-items: center;
}

.nav-item {
  margin: 0 15px;
  text-decoration: none;
  color: black;
  font-weight: bold;
}

.create-btn {
  background-color: black;
  color: white;
  padding: 10px 15px;
  border-radius: 20px;
  font-size: 14px;
}

.profile-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}
</style>
