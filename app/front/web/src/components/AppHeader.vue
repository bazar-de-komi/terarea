<!-- <template>
  <header :style="{ backgroundColor: backgroundColor }" class="header">
    <img src="@/assets/logo.png" class="logo" />
    <nav class="nav">
      <router-link to="/explore" class="nav-item">Explore</router-link>
      <router-link to="/my-applets" class="nav-item">MyApplets</router-link>
      <router-link to="/create" class="nav-item create-btn">Create</router-link>
      <img src="@/assets/profile-icon.svg" alt="Profile" class="profile-icon" />
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'AppHeader',
  props: {
    backgroundColor: {
      type: String as PropType<string>,
      default: 'white',
    },
  },
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.logo {
  width: 120px;
  height: auto;
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
</style> -->

<template>
  <header class="header">
    <img src="@/assets/logo.png" alt="Logo" class="logo" />
    <nav class="nav">
      <router-link to="/explore" class="nav-item">Explore</router-link>
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
  width: 100%;
  padding: 20px;
  z-index: 1000;
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
