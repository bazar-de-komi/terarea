<template>
  <div class="create-applet-page">
    <header>
      <AppHeader />
      <CancelButton @click="goBack" />
    </header>

    <div class="applet-creation">
      <h1>Create</h1>

      <div class="ifThenContainer">
        <!-- Bloc If -->
        <div class="ifThenBlock" @click="togglePhase('if')">
          <span class="block-text">If</span>
          <AddButton
            v-if="!ifCondition && !isSecondPhase.if"
            @click="showAddServiceModalForIf"
            :route="'/create/add-action'"
            class="add-button-right"
          />
          <span v-else class="selected-service">{{ ifCondition?.name || 'No service selected' }}</span>
        </div>
        <BlockDetails
        v-if="isSecondPhase.if"
        :title="ifCondition?.title || 'Default Title'"
        :description="ifCondition?.description || 'Default Description'"
        :fieldsData="['Dropdown:ServiceType', 'Date:StartDate', 'Time:StartTime', 'Input:Username', 'int:Age']"
        :blockWidth="800"
        />

        <!-- Bloc Then -->
        <div class="ifThenBlock" @click="togglePhase('then')">
          <span class="block-text">Then</span>
          <AddButton
            v-if="!thenAction && !isSecondPhase.then"
            @click="showAddServiceModalForThen"
            :route="'/create/add-reaction'"
            class="add-button-right"
          />
          <span v-else class="selected-service">{{ thenAction?.name || 'No action selected' }}</span>
        </div>
        <BlockDetails
        v-if="isSecondPhase.then"
          :title="ifCondition?.title || 'Default Title'"
          :description="ifCondition?.description || 'Default Description'"
          :fieldsData="['Dropdown:ServiceType', 'Date:StartDate', 'Time:StartTime', 'Input:Username', 'int:Age']"
          :blockWidth="800"
        />

      </div>
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
import BlockDetails from '@/components/CreateApplet-Comp/BlockDetails.vue';
import AddButton from '@/components/CreateApplet-Comp/AddDelButtonComp.vue';
import CancelButton from '@/components/CancelButton.vue';

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    AddButton,
    BlockDetails,
  },
  setup() {
    const router = useRouter();
    const ifCondition = ref(null);
    const thenAction = ref(null);
    const isModalOpen = ref(false);
    const currentBlock = ref('');
    const isSecondPhase = ref({ if: false, then: false });

    const goBack = () => {
      router.back();
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

    const togglePhase = (block: 'if' | 'then') => {
      isSecondPhase.value[block] = !isSecondPhase.value[block];
    };

    return {
      ifCondition,
      thenAction,
      isModalOpen,
      currentBlock,
      isSecondPhase,
      goBack,
      showAddServiceModalForIf,
      showAddServiceModalForThen,
      handleServiceSelection,
      closeModal,
      togglePhase,
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
  font-size: 3em;
  font-weight: bold;
  margin-bottom: 20px;
}

.ifThenContainer {
  padding-top: 10%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 100px;
}

.ifThenBlock {
  background-color: black;
  color: white;
  padding: 20px;
  border-radius: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 800px;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.ifThenBlock:nth-child(2) {
  background-color: grey;
}

.block-text, .selected-service {
  font-weight: bold;
  font-size: 64px;
  white-space: nowrap;
  flex-grow: 1;
  text-align: center;
}

.add-button-right {
  position: absolute;
  right: 15px;
}
</style>
