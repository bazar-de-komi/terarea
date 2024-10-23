<template>
  <div>
    <AppHeader />

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
import AppHeader from '@/components/AppHeader.vue';

interface Applet {
  title: string;
  description: string;
  source: string;
  userCount: number;
  color: string;
}

export default defineComponent({
  components: {
    AppHeader,
  },
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
