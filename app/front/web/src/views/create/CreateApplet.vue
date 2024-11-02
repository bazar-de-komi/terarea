<template>
  <div class="create-applet-page">
    <header>
      <AppHeader />
      <CancelButton @click="goBack" />
    </header>

    <div class="applet-creation">
      <h1>Create</h1>

      <IfBlock
        :serviceSelected="ifCondition?.name || ''"
        @add-service="showAddServiceModalForIf"
      />

      <div class="connector">
        <span>+</span>
      </div>

      <ThenBlock
        v-if="true"
        :serviceSelected="thenAction?.name || ''"
        @add-service="showAddServiceModalForThen"
        :showAddButton="ifCondition !== null"
      />
    </div>

    <AddServiceModal
      v-if="isModalOpen"
      @select-service="handleServiceSelection"
      @close="closeModal"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import IfBlock from '@/components/CreateApplet-Comp/IfBlock.vue';
import ThenBlock from '@/components/CreateApplet-Comp/ThenBlock.vue';
import CancelButton from '@/components/CancelButton.vue';
import AddServiceModal from '@/components/CreateApplet-Comp/AddServiceModal.vue';

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    IfBlock,
    ThenBlock,
    AddServiceModal,
  },
  setup() {
    const router = useRouter();
    const ifCondition = ref(null);
    const thenAction = ref(null);
    const isModalOpen = ref(false);
    const currentBlock = ref('');

    const goBack = () => {
      router.push('/explore/all');
    };

    const showAddServiceModalForIf = () => {
      currentBlock.value = 'if';
      isModalOpen.value = true;
    };

    const showAddServiceModalForThen = () => {
      currentBlock.value = 'then';
      isModalOpen.value = true;
    };

    const handleServiceSelection = (service: any) => {
      if (currentBlock.value === 'if') {
        ifCondition.value = service;
      } else if (currentBlock.value === 'then') {
        thenAction.value = service;
      }
      closeModal();
    };

    const closeModal = () => {
      isModalOpen.value = false;
    };

    return {
      ifCondition,
      thenAction,
      isModalOpen,
      currentBlock,
      goBack,
      showAddServiceModalForIf,
      showAddServiceModalForThen,
      handleServiceSelection,
      closeModal,
    };
  }
});
</script>

<style scoped>
.create-applet-page {
  font-family: Arial, sans-serif;
  padding: 20px;
}

.applet-creation {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

h1 {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 20px;
}

.connector {
  margin: 20px 0;
}

.connector span {
  font-size: 2em;
  font-weight: bold;
}
</style>
