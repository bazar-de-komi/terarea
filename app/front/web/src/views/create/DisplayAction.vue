<template>
  <div class="choose-service-page">
    <header class="header">
      <CancelButton buttonText="Back" @click="goBack" class="cancel-button" />
      <h1 class="page-title">Choose a Reaction</h1>
    </header>

    <div class="search-section">
      <input type="text" class="search-bar" placeholder="Search Reaction" v-model="searchQuery" />
      <button class="clear-search" @click="clearSearchQuery">✖</button>
    </div>

    <div class="divider"></div>

    <section class="tiles-section">
      <div class="tiles-grid">
        <TileComponent v-for="(tile, index) in filteredTiles" :key="index" :title="tile.json.name"
          :name="tile.serviceInfo?.name" :description="tile.json.description"
          @tile-selected="handleTileSelection(tile)" />
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import CancelButton from '@/components/CancelButton.vue';
import TileComponent from '@/components/CreateApplet-Comp/TileAct-ReactComp.vue';
import { queries } from '@/../lib/querier';

export default defineComponent({
  components: {
    CancelButton,
    TileComponent,
  },
  setup() {
    const router = useRouter();
    const searchQuery = ref('');
    const tiles = ref<any[]>([]);

    const goBack = () => {
      router.back();
    };

    const clearSearchQuery = () => {
      searchQuery.value = '';
    };

    // const filteredTiles = computed(() => {
    //   return tiles.value.filter(tile =>
    //     tile.json.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    //   );
    // });

    const filteredTiles = computed(() =>
      !searchQuery.value
        ? tiles.value
        : tiles.value.filter((tile) => {
          const searchWords = searchQuery.value.toLowerCase().split(' ').filter(word => word.length > 0);
          const matchesName = searchWords.some(word =>
            tile.json.name.toLowerCase().includes(word)
          );
          const matchesDescription = searchWords.some(word =>
              tile.json.description.toLowerCase().split(' ').some((description_word: string) => description_word.includes(word))
          );
          const matchesService = searchWords.some(word =>
            tile.serviceInfo.name.toLowerCase().includes(word)
          );
          return matchesName || matchesService || matchesDescription;
        })
    );

    const handleTileSelection = (tileData: any) => {
      router.push({ name: 'ReactionInformation', query: { tile: JSON.stringify(tileData) } });
    };

    onBeforeMount(async () => {
      try {
        const token = localStorage.getItem("authToken") || "";
        const reactions_response = await queries.get("/api/v1/reactions", {}, token);
        if (reactions_response.resp === "success") {
          tiles.value = reactions_response.msg;
          await Promise.all(
            tiles.value.map(async (tile: any, index: number) => {
              try {
                const getServiceNameResponse = await queries.get(`/api/v1/service/${tile.service_id}`, {}, token);
                if (getServiceNameResponse.resp === "success") {
                  tiles.value[index] = {
                    ...tile,
                    serviceInfo: getServiceNameResponse.msg,
                  };
                }
              } catch (error) {
                console.error(`Erreur pour récupérer les données pour la tile ${tile.id}:`, error);
              }
            })
          );
        }
      } catch (error) {
        console.error("Error when charging reactions:", error);
      }
    });

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
.tile {
  color: #333;
  background-color: #ff61fc;
}

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
