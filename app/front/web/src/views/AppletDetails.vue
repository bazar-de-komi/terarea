<template>
  <div>
    <header class="header">
      <img src="@/assets/logo.png"/>
      <nav class="nav">
        <router-link to="/explore" class="nav-item">Explore</router-link>
        <router-link to="/my-applets" class="nav-item">MyApplets</router-link>
        <router-link to="/create" class="nav-item create-btn">Create</router-link>
        <img src="@/assets/profile-icon.svg" alt="Profile" class="profile-icon" />
      </nav>
    </header>

    <div class="applet-details" :style="{ backgroundColor: applet.color }">
      <h1 class="applet-title">{{ applet.title }}</h1>
      <p class="applet-source">by {{ applet.source }}</p>
      <div class="applet-stats">
        <span class="users-count">{{ applet.userCount }} users</span>
      </div>
      <button class="connect-btn">Connect</button>
      <p class="applet-description">{{ applet.description }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

interface Applet {
  title: string;
  description: string;
  source: string;
  userCount: number;
  color: string;
}

export default defineComponent({
  setup() {
    const route = useRoute();
    const store = useStore();

    const applet = computed<Applet | undefined>(() => {
      const title = Array.isArray(route.params.title) ? route.params.title[0] : route.params.title;
      const formattedTitle = title.replace(/-/g, ' ');
      return store.state.applets.applets.find((applet: Applet) => applet.title.toLowerCase() === formattedTitle.toLowerCase());
    });

    return {
      applet,
    };
  },
});
</script>


<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.logo {
  width: 80px;
}

.nav {
  display: flex;
  align-items: center;
}

.nav-item {
  margin: 0 15px;
  text-decoration: none;
  color: white;
  font-weight: bold;
}

.create-btn {
  background-color: white;
  color: black;
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

.applet-details {
  padding: 120px 20px;
  text-align: center;
  color: white;
}

.applet-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.applet-source {
  font-size: 1.1rem;
  color: #888;
}

.applet-stats {
  margin: 10px 0;
}

.users-count {
  background-color: #333;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.9rem;
}

.connect-btn {
  background-color: black;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 12px 25px;
  margin: 15px 0;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.applet-description {
  color: #bbb;
  font-size: 1rem;
  margin-top: 10px;
}
</style>
