<template>
  <div class="create-applet-page">
    <header>
      <AppHeader /> <!-- Composant pour le header -->
      <div class="cancel-button-container">
        <CancelButton @click="goBack" />
      </div>
    </header>

    <div class="applet-creation">
      <h1>Create</h1>
      <p class="applet-count">You're using {{ appletCount }} of 2 Applets</p>

      <!-- Bloc If -->
      <IfBlock
        :condition="applet.ifCondition"
        @edit="editCondition"
        @delete="deleteCondition"
        @service-selected="updateIfBlock"
      />

      <div class="connector">
        <span>+</span>
      </div>

      <!-- Bloc Then -->
      <ThenBlock
        :action="applet.thenAction"
        @add="addAction"
        @service-selected="updateThenBlock"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import IfBlock from '@/components/IfBlock.vue';
import ThenBlock from '@/components/ThenBlock.vue';
import CancelButton from '@/components/CancelButton.vue';

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    IfBlock,
    ThenBlock
  },
  setup() {
    const router = useRouter();
    const applet = ref({
      ifCondition: {},
      thenAction: {}
    });
    const appletCount = ref(0);

    const fetchAppletData = async () => {
      try {
        const response = await fetch('/api/applet-data');
        const data = await response.json();
        applet.value = data;
        appletCount.value = data.length;
      } catch (error) {
        console.error('Erreur lors du chargement des données :', error);
      }
    };

    onMounted(() => {
      fetchAppletData();
    });

    const goBack = () => {
      router.push('/explore/all');  // Redirection vers une autre page
    };

    const updateIfBlock = (service: any) => {
      applet.value.ifCondition = service;
    };

    const updateThenBlock = (service: any) => {
      applet.value.thenAction = service;
    };

    return {
      applet,
      appletCount,
      updateIfBlock,
      updateThenBlock,
      goBack
    };
  }
});
</script>

<style scoped>
.create-applet-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 10px 50px;
  position: relative;
}

.cancel-button-container {
  position: absolute;
  top: 80px;
  left: 60px;
}

.applet-creation {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 100px;
}

h1 {
  margin-bottom: 20px;
}

.connector {
  margin: 20px 0;
  font-size: 2rem;
}

.applet-count {
  margin: 20px 0;
  font-size: 1rem;
}
</style>
