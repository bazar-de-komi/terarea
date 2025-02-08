<template>
  <div class="create-applet-page">
    <header>
      <AppHeader />
      <CancelButton @click="goBack" />
    </header>

    <div class="applet-creation">
      <h1>Create</h1>

      <div class="ifThenContainer">
        <div class="ifThenBlock" @click="goToAddTrigger">
          <span class="block-text">If</span>
          <AddButton v-if="!ifCondition" class="add-button-right" />
          <span v-else class="selected-service">{{ ifCondition.json.name }}</span>
        </div>

        <div class="ifThenBlock" :class="{ disabled: !ifCondition }" @click="ifCondition && goToAddAction()">
          <span class="block-text">Then</span>
          <AddButton v-if="ifCondition && !thenAction" class="add-button-right" />
          <span v-else-if="thenAction" class="selected-service">{{ thenAction.json.name }}</span>
        </div>
      </div>

      <div v-if="ifCondition && thenAction">
        <label>Your applet name</label>
        <input v-model="applet_name" placeholder="Enter applet name" />

        <label>Your applet description</label>
        <input v-model="applet_description" placeholder="Enter applet description" />

        <label>Your applet tags (Optional)</label>
        <input v-model="applet_tags" placeholder="Enter tags" />

        <label>Your applet colour</label>
        <input type="color" v-model="applet_colour" />
      </div>

      <CreateButton v-if="ifCondition && thenAction && applet_name && applet_description && applet_colour"
        @create="handleCreateApplet" />
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
import { queries } from '@/../lib/querier';

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

    const applet_name = ref('');
    const applet_description = ref('');
    const applet_tags = ref('');
    const applet_colour = ref('#ffffff');

    const goBack = () => {
      sessionStorage.removeItem('selectedTrigger');
      sessionStorage.removeItem('selectedAction');
      router.push('/explore/applets');
    };

    const goToAddTrigger = () => {
      router.push('/create/add-trigger');
    };

    const goToAddAction = () => {
      if (ifCondition.value) {
        router.push('/create/add-action');
      }
    };

    const handleCreateApplet = async () => {
      const storedTrigger = JSON.parse(sessionStorage.getItem('selectedTrigger') || "");
      const storedAction = JSON.parse(sessionStorage.getItem('selectedAction') || "");
      try {
        const token = localStorage.getItem("authToken") || "";
        const response = await queries.post(
          "/api/v1/my_applet",
          {
            name: applet_name.value,
            trigger: storedTrigger?.json,
            consequences: storedAction?.json,
            tags: applet_tags.value,
            description: applet_description.value,
            colour: applet_colour.value
          },
          token
        );
        if (response.resp === "success") {
          alert('Applet créé avec succès !');
          sessionStorage.removeItem('selectedTrigger');
          sessionStorage.removeItem('selectedAction');
          router.push('/explore/applets');
        }
      } catch (error) {
        alert('Failed to create the new applet.');
        return;
      }
    };

    watchEffect(() => {
      const triggerData = route.query.trigger;
      if (!ifCondition.value && typeof triggerData === 'string') {
        try {
          ifCondition.value = JSON.parse(triggerData);
          sessionStorage.setItem('selectedTrigger', triggerData);
        } catch (error) {
          console.error('Erreur de parsing du déclencheur:', error);
        }
      } else if (!ifCondition.value) {
        const storedTrigger = sessionStorage.getItem('selectedTrigger');
        if (storedTrigger) {
          ifCondition.value = JSON.parse(storedTrigger);
        }
      }

      const actionData = route.query.action;
      if (!thenAction.value && typeof actionData === 'string') {
        try {
          thenAction.value = JSON.parse(actionData);
          sessionStorage.setItem('selectedAction', actionData);
        } catch (error) {
          console.error('Erreur de parsing de l\'action:', error);
        }
      } else if (!thenAction.value) {
        const storedAction = sessionStorage.getItem('selectedAction');
        if (storedAction) {
          thenAction.value = JSON.parse(storedAction);
        }
      }
    });

    onMounted(() => {
      ifCondition.value = JSON.parse(sessionStorage.getItem('selectedTrigger') || 'null');
      thenAction.value = JSON.parse(sessionStorage.getItem('selectedAction') || 'null');
    });

    return {
      ifCondition,
      thenAction,
      goBack,
      goToAddTrigger,
      goToAddAction,
      handleCreateApplet,
      applet_name,
      applet_description,
      applet_tags,
      applet_colour
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

/* Inputs */
label {
  font-size: 1rem;
  font-weight: 500;
  color: #555;
  display: block;
  margin: 10px 0 5px;
  text-align: left;
  width: 100%;
}

input {
  width: 100%;
  max-width: 600px;
  padding: 12px;
  font-size: 1rem;
  border: 2px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s ease;
}

input:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.2);
}

/* Input couleur */
input[type="color"] {
  width: 60px;
  height: 40px;
  padding: 5px;
  border: none;
  cursor: pointer;
}
</style>
