<template>
  <div class="explore-page">
    <AppHeader backgroundColor="#f0f0f0" />
    <Header />
    <section class="title-section">
      <h1 class="section-title">Explore</h1>
      <div class="filter-buttons">
        <router-link to="/explore/all" class="filter-btn" :class="{ active: $route.path === '/explore/all' }">All</router-link>
        <router-link to="/explore/applets" class="filter-btn" :class="{ active: $route.path === '/explore/applets' }">Applets</router-link>
        <router-link to="/explore/services" class="filter-btn active" :class="{ active: $route.path === '/explore/services' }">Services</router-link>
      </div>
    </section>
    <div class="search-section">
      <input
        type="text"
        class="search-bar"
        placeholder="Search Applets or services"
        v-model="searchQuery"
        @input="updateSearchQuery"
      />
      <button class="clear-search" @click="clearSearchQuery">✖</button>
    </div>
    <section class="applets-section">
      <div class="applets-container">
        <div class="applets-grid" ref="appletsGrid">
          <AppletTile
            v-for="(applet, index) in filteredApplets"
            :key="index"
            :title="applet.title"
            :description="applet.description"
            :background-color="applet.color"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';
import Header from '@/components/AppHeader.vue';
import AppletTile from '@/components/AppletTile.vue';

export default defineComponent({
  components: {
    Header,
    AppletTile,
  },
  setup() {
    const store = useStore();

    const searchQuery = computed({
      get: () => store.state.applets.searchQuery,
      set: (value: string) => store.dispatch('applets/updateSearchQuery', value),
    });

    const filteredApplets = computed(() => store.getters['applets/filteredApplets']);

    const updateSearchQuery = () => {
      store.dispatch('applets/updateSearchQuery', searchQuery.value);
    };

    const clearSearchQuery = () => {
      store.dispatch('applets/updateSearchQuery', '');
    };

    return {
      searchQuery,
      filteredApplets,
      updateSearchQuery,
      clearSearchQuery,
    };
  },
});
</script>


<style scoped>
.filter-btn.active {
  font-weight: bold;
}

.explore-page {
  font-family: 'Arial', sans-serif;
  padding: 0 10px;
  background-color: white;
  padding-top: 100px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
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

.title-section {
  text-align: center;
  margin: 30px 0;
}

.section-title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.filter-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.filter-btn {
  background-color: transparent;
  border: none;
  color: black;
  font-size: 18px;
  margin: 0 10px;
  cursor: pointer;
}

.filter-btn:hover {
  text-decoration: underline;
}

.search-section {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.search-bar {
  width: 600px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 16px;
  text-align: center;
}

.clear-search {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: -35px;
  font-size: 18px;
}

.applets-section {
  text-align: center;
}

.applets-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.applets-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  scroll-behavior: smooth;
  padding: 20px 0;
  max-width: 90%;
}

.applet-tile {
  width: 250px;
  height: 300px;
  background-color: var(--tile-background-color, #f1f1f1);
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.applet-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.applet-description {
  font-size: 16px;
  color: #666;
  line-height: 1.5;
}
</style>
