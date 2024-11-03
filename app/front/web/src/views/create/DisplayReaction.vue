<template>
  <div class="choose-service-page">
    <header class="header">
      <CancelButton buttonText="Back" @click="goBack" class="cancel-button" />
      <h1 class="page-title">Choose an Reaction</h1>
    </header>

    <div class="search-section">
      <input
        type="text"
        class="search-bar"
        placeholder="Search Reaction"
        v-model="searchQuery"
      />
      <button class="clear-search" @click="clearSearchQuery">✖</button>
    </div>

    <div class="divider"></div>

    <section class="tiles-section">
      <div class="tiles-grid">
        <TileComponent
          v-for="(tile, index) in filteredTiles"
          :key="index"
          :title="tile.title"
          :description="tile.description"
          :backgroundColor="tile.backgroundColor"
          :name="tile.name"
          @tile-selected="handleTileSelection"
        />
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import CancelButton from '@/components/CancelButton.vue';
import TileComponent from '@/components/CreateApplet-Comp/TileAct-ReactComp.vue';

export default defineComponent({
  components: {
    CancelButton,
    TileComponent,
  },
  setup() {
    const router = useRouter();
    const searchQuery = ref('');

    const goBack = () => {
      router.back();
    };

    const clearSearchQuery = () => {
      searchQuery.value = '';
    };

    const tiles = ref([
      { title: 'New status message on page', description: 'This Trigger fires every time you create a new status message on your Facebook Page.', backgroundColor: '#3b5998', name: 'Facebook' },
      { title: 'New status message with hashtag on page', description: 'This Trigger fires every time you create a new status message with a specific hashtag on your Facebook Page.', backgroundColor: '#3b5998', name: 'Facebook' },
      // Ajoutez d'autres tuiles ici
    ]);

    const filteredTiles = computed(() => {
      return tiles.value.filter(tile =>
        tile.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const handleTileSelection = (tileData: any) => {
      router.push({ name: 'CreateApplet', params: { selectedTile: tileData } });
    };

    return {
      searchQuery,
      goBack,
      clearSearchQuery,
      filteredTiles,
      handleTileSelection,
    };
  },
});
</script>

<style scoped>
.choose-service-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 20px;
}

.cancel-button {
  margin-top: -80px;
  margin-right: auto;
}

.page-title {
  margin: 0 auto;
  font-size: 2rem;
  font-weight: bold;
}


.search-section {
  display: flex;
  align-items: center;
  margin-top: 80px;
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-bar {
  width: 100%;
  padding: 15px 20px;
  font-size: 1.1rem;
  border: 2px solid #ccc;
  border-radius: 25px;
  outline: none;
  text-align: center;
}

.search-bar:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.25);
}

.clear-search {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: -35px;
  font-size: 18px;
}

.divider {
  margin: 50px auto;
  width: 80%;
  height: 4px;
  background-color: #ddd;
  border-radius: 2px;
}

.tiles-section {
  text-align: center;
}

.tiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px 0;
  max-width: 1200px;
  margin: 0 auto;
}

.tile-component {
  background-color: #333;
  color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: Arial, sans-serif;
  min-height: 180px;
  text-align: left;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.tile-component:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.tile-component h2 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.tile-component p {
  font-size: 0.9rem;
  line-height: 1.4;
}

@media (min-width: 1200px) {
  .tiles-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .tiles-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 991px) {
  .tiles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .tiles-grid {
    grid-template-columns: 1fr;
  }
}
</style>