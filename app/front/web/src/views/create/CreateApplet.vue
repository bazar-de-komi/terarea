<template>
  <div class="create-applet-page">
    <header>
      <AppHeader />
      <CancelButton @click="goBack" />
    </header>

    <div class="applet-creation">
      <h1>Create</h1>

      <div class="ifThenContainer">
        <div
          class="ifThenBlock"
          @click="goToAddTrigger"
        >
          <span class="block-text">If</span>
          <AddButton v-if="!ifCondition" class="add-button-right" />
          <span v-else class="selected-service">{{ ifCondition.name }}</span>
        </div>

        <div
          class="ifThenBlock"
          :class="{ disabled: !ifCondition }"
          @click="ifCondition && goToAddAction()"
        >
          <span class="block-text">Then</span>
          <AddButton v-if="ifCondition && !thenAction" class="add-button-right" />
          <span v-else-if="thenAction" class="selected-service">{{ thenAction.name }}</span>
        </div>
      </div>

      <CreateButton v-if="ifCondition && thenAction" @create="handleCreateApplet" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watchEffect, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import AddButton from '@/components/CreateApplet-Comp/AddDelButtonComp.vue';
import CancelButton from '@/components/CancelButton.vue';
import CreateButton from '@/components/CreateApplet-Comp/CreateButton.vue';

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    AddButton,
    CreateButton,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const ifCondition = ref<any>(null);
    const thenAction = ref<any>(null);

    const goBack = () => {
      router.back();
    };

    const goToAddTrigger = () => {
      router.push('/create/add-trigger');
    };

    const goToAddAction = () => {
      if (ifCondition.value) {
        router.push('/create/add-action');
      }
    };

    const handleCreateApplet = () => {
      alert('Applet créé avec succès !');
      localStorage.removeItem('selectedTrigger');
      localStorage.removeItem('selectedAction');
      router.push('/explore/applets');
    };

    watchEffect(() => {
      const triggerData = route.query.trigger;
      if (!ifCondition.value && typeof triggerData === 'string') {
        try {
          ifCondition.value = JSON.parse(triggerData);
          localStorage.setItem('selectedTrigger', triggerData);
        } catch (error) {
          console.error('Erreur de parsing du déclencheur:', error);
        }
      } else if (!ifCondition.value) {
        const storedTrigger = localStorage.getItem('selectedTrigger');
        if (storedTrigger) {
          ifCondition.value = JSON.parse(storedTrigger);
        }
      }

      const actionData = route.query.action;
      if (!thenAction.value && typeof actionData === 'string') {
        try {
          thenAction.value = JSON.parse(actionData);
          localStorage.setItem('selectedAction', actionData);
        } catch (error) {
          console.error('Erreur de parsing de l\'action:', error);
        }
      } else if (!thenAction.value) {
        const storedAction = localStorage.getItem('selectedAction');
        if (storedAction) {
          thenAction.value = JSON.parse(storedAction);
        }
      }
    });

    onMounted(() => {
      ifCondition.value = JSON.parse(localStorage.getItem('selectedTrigger') || 'null');
      thenAction.value = JSON.parse(localStorage.getItem('selectedAction') || 'null');
    });

    return {
      ifCondition,
      thenAction,
      goBack,
      goToAddTrigger,
      goToAddAction,
      handleCreateApplet,
    };
  },
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
  background-color: rgb(60, 59, 59);
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

.ifThenBlock.disabled {
  background-color: grey;
  cursor: not-allowed;
}

.block-text,
.selected-service {
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
