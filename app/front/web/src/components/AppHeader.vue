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
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 25px;
  z-index: 1000;
  font-family: 'Arial', sans-serif;
  box-sizing: border-box;
  background-color: transparent;
}

.logo {
  width: 120px;
}

.nav {
  display: flex;
  align-items: center;
}

.nav-item {
  margin: 0 20px;
  text-decoration: none;
  color: black;
  font-weight: bold;
  font-size: 16px;
}

.create-btn {
  background-color: black;
  color: white;
  padding: 12px 18px;
  border-radius: 25px;
  font-size: 16px;
}

.profile-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
}
</style>
