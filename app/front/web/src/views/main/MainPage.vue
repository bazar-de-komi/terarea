<template>
  <div class="main-page">
    <!-- Inclure le header que nous avons créé -->
    <AppHeaderMain />

    <!-- Image de fond en position absolue -->
    <div class="background-image"></div>

    <!-- Contenu principal de la page -->
    <div class="content">
      <!-- Contenu spécifique de la page principale -->
      <h1>Automation for business and home</h1>
      <p>Save time and get more done</p>
      <button class="start-btn">Start Today</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AppHeaderMain from '@/views/main/AppHeaderMain.vue';

export default defineComponent({
  name: 'MainPage',
  components: {
    AppHeaderMain,
  },
});
</script>

<style scoped>
.main-page {
  position: relative;
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
  height: 60vh; /* Premier tiers de la page */
  background-image: url('@/assets/background.jpg'); /* Remplacer avec le chemin de votre image */
  background-size: cover;
  background-position: center;
  z-index: -1; /* Derrière le contenu principal */
}

/* Contenu principal centré */
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 65vh; /* Place le contenu en dessous de l'image */
  text-align: center;
}

.content h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 10px;
}

.content p {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 20px;
}

.start-btn {
  background-color: black;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  font-size: 1em;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-btn:hover {
  background-color: #333;
}
</style>
