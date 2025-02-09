<template>
  <div class="main-page">
    <AppHeaderMain />

    <div class="background-image"></div>

    <div class="content">
      <h1>Automation for business and home</h1>
      <p>Save time and get more done</p>
      <router-link to="/sign-up" class="start-btn">Start Today</router-link>
    </div>

    <!-- Section des Applets -->
    <section class="applets-section">
      <h2 class="applets-title">Get started with any Applet</h2>

      <div class="applets-container">
        <div class="applets-grid">
          <AppletTile
            v-for="(applet, index) in filteredServices.slice(0, 4)"
            :key="index"
            :title="applet.title"
            :backgroundColor="applet.color"
          />
        </div>
      </div>

      <h2 class="applets-title">... or choose from 4+ services</h2>

      <div class="applets-container">
        <div class="applets-grid">
          <AppletTile
            v-for="(applet, index) in filteredServices.slice(0, 4)"
            :key="index"
            :title="applet.title"
            :backgroundColor="applet.color"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';
import AppHeaderMain from '@/components/Main-Page-Comp/AppHeaderMain.vue';
import AppletTile from '@/components/Main-Page-Comp/AppletsDisplay.vue';

export default defineComponent({
  name: 'MainPage',
  components: {
    AppHeaderMain,
    AppletTile,
  },
  setup() {
    const store = useStore();

    const filteredApplets = computed(() => store.getters['applets/filteredApplets']);
    const filteredServices = computed(() => store.getters['applets/filteredServices']);

    return {
      filteredApplets,
      filteredServices,
    };
  },
});
</script>

<style scoped>
.main-page {
  width: 100%;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
}

/* Image de fond */
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 60vh;
  background-image: linear-gradient(
      rgba(0, 0, 0, 0.5),
      rgba(0, 0, 0, 0.5)
    ),
    url('@/assets/background.jpg');
  background-size: cover;
  background-position: center;
  z-index: -1;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  transition: height 0.4s ease;
}

/* Contenu principal centré */
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 15vh;
  text-align: center;
}

.content h1 {
  font-size: 4.5em;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: -10px;
  text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.6);
}

.content p {
  font-size: 2em;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 60px;
  text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.9);
}

.start-btn {
  background-color: rgba(255, 255, 255, 0.95);
  color: rgba(0, 0, 0, 0.8);
  padding: 25px 60px;
  border: none;
  border-radius: 60px;
  font-size: 3em;
  font-weight: bold;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-btn:hover {
  background-color: rgba(153, 153, 153, 0.9);
}

.applets-title {
  font-size: 2.5em;
  font-weight: bold;
  color: #333;
  margin-top: 40px;
  text-align: center;
}

.applets-description {
  font-size: 1.2em;
  color: #666;
  margin-top: 10px;
  margin-bottom: 30px;
  text-align: center;
}

.applets-footer {
  font-size: 1.2em;
  color: #666;
  margin-top: 30px;
  text-align: center;
}

.applets-section {
  text-align: center;
  position: relative;
  margin-top:150px;
}

.applets-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.applets-grid {
  display: grid;
  gap: 20px;
  padding: 20px 0;
  max-width: 100%;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: auto;
  overflow: hidden;
}

.applets-grid > * {
  height: auto;
}

@media (min-width: 1200px) {
  .applets-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .applets-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .background-image {
    height: 60vh;
  }
}

@media (min-width: 768px) and (max-width: 991px) {
  .applets-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .background-image {
    height: 60vh;
  }
}

@media (max-width: 767px) {
  .applets-grid {
    grid-template-columns: 1fr;
  }
  .background-image {
    height: 70vh;
  }
}
</style>
