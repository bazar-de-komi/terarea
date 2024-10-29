<template>
  <div>
    <header>
      <AppHeader />
      <CancelButton @click="goBack" />
    </header>

    <!-- Première boîte (service-header) -->
    <div ref="serviceHeader" class="service-header" :style="{ backgroundColor: service.color }">
      <CompTitle :title="service.title" />
      <CompDescription :description="service.description" />
    </div>

    <!-- Section des Applets -->
    <section class="applets-section" :style="{ marginTop: `${appletsSectionTop}px` }">
      <div class="applets-container">
        <div class="applets-grid" ref="appletsGrid">
          <template v-for="(item, index) in filteredApplets" :key="index">
            <AppletTile
              v-if="item.type === 'applet'"
              :title="item.title"
              :background-color="item.color"
            />
          </template>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import CancelButton from '@/components/CancelButton.vue';
import CompTitle from '@/components/Details-Service/CompTitle.vue';
import CompDescription from '@/components/Details-Service/CompDescription.vue';
import AppletTile from '@/components/AppletBoardTile.vue';

interface Service {
  title: string;
  description: string;
  source: string;
  userCount: number;
  color: string;
}

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    CompTitle,
    CompDescription,
    AppletTile,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const serviceHeader = ref<HTMLDivElement | null>(null);
    const appletsSectionTop = ref(0);

    const service = computed<Service | undefined>(() => {
      const title = Array.isArray(route.params.title) ? route.params.title[0] : route.params.title;
      const formattedTitle = title.replace(/-/g, ' ');
      return store.state.applets.applets.find((applet: Service) => applet.title.toLowerCase() === formattedTitle.toLowerCase());
    });

    const goBack = () => {
      router.push('/explore/all');
    };

    const filteredApplets = computed(() => store.getters['applets/filteredApplets']);

    onMounted(() => {
      if (serviceHeader.value) {
        appletsSectionTop.value = serviceHeader.value.offsetHeight;
      }
    });

    return {
      service,
      goBack,
      filteredApplets,
      appletsSectionTop,
      serviceHeader,
    };
  },
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.service-header {
  padding: 50px 30px;
  width: 100%;
  min-height: 400px;
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  z-index: 1;
  top: 0;
  left: 0;
  right: 0;
  position: absolute;
}

.cancel-button {
  color: white;
  background-color: black;
  z-index: 3;
}

.cancel-button:hover {
  background-color: #212121;
  transform: scale(1.05);
}

.service-title {
  font-size: 3em;
  font-weight: bold;
  margin-top: 50px;
  margin-bottom: 20px;
  text-align: center;
  word-wrap: break-word;
  max-width: 40%;
  line-height: 1.2;
}

.service-source {
  font-size: 1.2em;
  margin-bottom: 10px;
  text-align: center;
}

.service-stats {
  font-size: 1em;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0;
}

.service-body {
  position: relative;
  top: 0;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  z-index: 2;
  width: 40%;
  max-width: 90%;
  margin: 0 auto;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  height: auto;
}

.connect-button {
  width: 100%;
  padding: 15px;
  font-size: 1.2em;
  margin: 20px 0;
  border-radius: 50px;
  text-align: center;
}

.service-description {
  font-size: 1.7em;
  margin-top: 20px;
  text-align: center;
  padding: 15px;
  color: white;
  font-weight: bold;
  background-color: transparent;
  border-radius: 10px;
  width: auto;
  max-width: auto;
  word-wrap: break-word;
}

.applets-section {
  text-align: center;
  position: relative; /* Permet de s'aligner en dessous de service-header */
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
  grid-auto-rows: minmax(100px, auto);
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
}

@media (min-width: 768px) and (max-width: 991px) {
  .applets-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .applets-grid {
    grid-template-columns: 1fr;
  }
}
</style>
