<template>
  <header class="header">
    <router-link to="/" class="logo-link">
      <img src="@/assets/logo.png" alt="Logo" class="logo" />
    </router-link>
    <nav class="nav">
      <router-link to="/explore/all" class="nav-item">Explore</router-link>
      <router-link to="/create" class="nav-item create-btn">Create</router-link>
      <!-- Icône de profil avec le menu déroulant -->
      <div class="profile-container" @click="toggleProfileMenu">
        <img src="@/assets/profile-icon.svg" alt="Profile" class="profile-icon" />
        <transition name="fade">
          <div v-if="isProfileMenuOpen" class="profile-menu">
            <router-link to="/account" class="menu-item">Account</router-link>
            <router-link to="/services" class="menu-item">My services</router-link>
            <div class="separator"></div>
            <router-link to="/help" class="menu-item">Help</router-link>
            <router-link to="/" class="menu-item logout" @click="logUserOut">Log out</router-link>
          </div>
        </transition>
      </div>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { queries } from '@/../lib/querier';

export default defineComponent({
  setup() {
    const isProfileMenuOpen = ref(false);

    const toggleProfileMenu = () => {
      isProfileMenuOpen.value = !isProfileMenuOpen.value;
    };

    return {
      isProfileMenuOpen,
      toggleProfileMenu,
    };
  },
  methods: {
    async logUserOut() {
      try {
        const token = localStorage.getItem("authToken") || "";
        await queries.post("/api/v1/logout", {}, token);
        localStorage.removeItem("authToken");
      } catch (error) {
        alert("Failed to logout.");
      }
    }
  }
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

.logo-link,
.profile-link {
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

.profile-container {
  position: relative;
}

.profile-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Style pour le menu déroulant amélioré */
.profile-menu {
  position: absolute;
  top: 60px;
  right: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  width: 180px;
  z-index: 1000;
  padding: 10px 0;
}

.menu-item {
  display: block;
  padding: 12px 20px;
  color: #333;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.separator {
  height: 1px;
  margin: 8px 0;
  background-color: #eee;
}

.logout {
  color: #d9534f;
}

.logout:hover {
  background-color: #f5f5f5;
}
</style>
