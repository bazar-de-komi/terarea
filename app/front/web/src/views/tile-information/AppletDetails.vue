<template>
  <div>
    <header>
      <AppHeader />
      <CancelButton buttonText="Back" @click="goBack" />
    </header>

    <!-- Première boîte (applet-header) -->
    <div class="applet-header" :style="{ backgroundColor: applet?.color }">
      <CompTitle :title="applet?.title || ''" />
    </div>

    <!-- Boîte contenant CompConnectButton et CompDescription -->
    <div class="applet-body" :style="{ backgroundColor: applet?.color }">
      <CompConnectButton :applet-id="applet?.id || 0" buttonColor="applet?.color || 'blue'" />
      <CompDescription :description="applet?.description || ''" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import CancelButton from '@/components/CancelButton.vue';
import CompTitle from '@/components/Details-Applet/CompTitle.vue';
import CompConnectButton from '@/components/Details-Applet/CompConnectButton.vue';
import CompDescription from '@/components/Details-Applet/CompDescription.vue';

interface Applet {
  id: number;
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
    CompConnectButton,
    CompDescription,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();

    const applet = computed<Applet | undefined>(() => {
      const title = Array.isArray(route.params.title) ? route.params.title[0] : route.params.title;
      const formattedTitle = title.replace(/-/g, ' ');
      return store.state.applets.applets.find((applet: Applet) => applet.title.toLowerCase() === formattedTitle.toLowerCase());
    });

    const goBack = () => {
      router.push('/explore/all');
    };

    return {
      applet,
      goBack,
    };
  }
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

.applet-header {
  padding: 50px 30px;
  width: 100%;
  min-height: 400px;
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
  height: auto;
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

.applet-title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  word-wrap: break-word;
  max-width: 40%;
  line-height: 1.2;
}

.applet-source {
  font-size: 1.2em;
  margin-bottom: 10px;
  text-align: center;
}

.applet-stats {
  font-size: 1em;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0;
}

.applet-body {
  position: relative;
  top: 500px;
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

.applet-description {
  font-size: 1.5em;
  margin-top: 20px;
  text-align: center;
  padding: 15px;
  color: white;
  font-weight: bold;
  background-color: transparent;
  border-radius: 10px;
  width: auto;
  max-width: 90%;
  word-wrap: break-word;
}
</style>

