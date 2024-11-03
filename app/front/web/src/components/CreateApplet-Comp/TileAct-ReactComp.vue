<template>
  <div class="tile" :style="{ backgroundColor: backgroundColor }" @click="selectTile">
    <h2 class="tile-title">{{ title }}</h2>
    <p class="tile-description">{{ description }}</p>
    <span class="tile-name">{{ name }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'TileComponent',
  props: {
    title: String,
    description: String,
    backgroundColor: String,
    name: String,
    details: Array as PropType<string[]>,
  },
  emits: ['tile-selected'],
  methods: {
    selectTile() {
      this.$emit('tile-selected', {
        title: this.title,
        description: this.description,
        backgroundColor: this.backgroundColor,
        name: this.name,
        fieldsData: this.details,
      });
    },
  },
});
</script>

<style scoped>
.tile {
  width: 100%;
  max-width: 250px; /* Largeur maximale pour des tuiles équilibrées */
  padding: 20px;
  border-radius: 10px;
  color: white;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  min-height: 180px;
  text-align: left;
  margin: 10px; /* Espace autour des tuiles */
}

/* Effet de survol pour ajouter du dynamisme */
.tile:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.tile-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.tile-description {
  font-size: 0.9rem;
  line-height: 1.4;
  flex-grow: 1;
}

.tile-name {
  font-size: 0.85rem;
  text-align: right;
  margin-top: 15px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
}

/* Disposition en grille pour les tuiles */
.tiles-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}
</style>
