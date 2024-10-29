<template>
  <div class="create-applet-page">
    <header>
      <AppHeader />
      <CancelButton @click="goBack" />
    </header>

    <div class="applet-creation">
      <h1>Create</h1>

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
import IfBlock from '@/components/CreateApplet-Comp/IfBlock.vue';
import ThenBlock from '@/components/CreateApplet-Comp/ThenBlock.vue';
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
      router.push('/explore/all');
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
