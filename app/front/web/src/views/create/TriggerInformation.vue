<template>
  <div class="trigger-page">
    <header>
      <CancelButton buttonText="Back" @click="goBack" class="cancel-button" />
    </header>

    <div class="service-header" :style="{ backgroundColor: '#ff61fc' }">
      <h1 class="service-title">{{ tileData?.json.name }}</h1>
      <p class="service-source">{{ tileData?.serviceInfo.name }}</p>
      <p class="service-description">{{ tileData?.json.description }}</p>
    </div>

    <div class="service-body">

      <template v-if="formFields.length">
        <div v-for="(field, index) in formFields" :key="index" class="form-group">
          <label :for="field.name">{{ field.name }}</label>
          <input v-if="field.type === 'input'" :id="field.name" type="text" v-model="field.value">
          <textarea v-else-if="field.type === 'textarea'" :id="field.name" type="text" v-model="field.value" />
          <select v-else-if="field.type === 'dropdown'" :id="field.name" v-model="field.defaultValue">
            <option v-for="option in field.options" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
        </div>
      </template>

      <button class="connect-button" @click="useTrigger">Use this Trigger</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import CancelButton from '@/components/CancelButton.vue';
import parseJsonToForm from '@/ParseJson';

export default defineComponent({
  components: {
    CancelButton,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const tileData = ref<any>(null);
    const formFields = ref<any[]>([]);

    const goBack = () => {
      router.back();
    };

    const useTrigger = () => {
      if (tileData.value) {
        localStorage.setItem('selectedTrigger', JSON.stringify(tileData.value));
      }
      router.push({
        path: '/create',
        query: { startSecondPhase: 'true' }
      });
    };

    const getDropdownModel = (field: any) => {
      return computed({
        get: () => field.value ?? field.defaultValue,
        set: (newValue) => field.value = newValue
      });
    };

    onMounted(() => {
      if (route.query.tile) {
        console.log(route.query.tile);
        try {
          tileData.value = JSON.parse(route.query.tile as string);
          console.log("TileData:", tileData.value);
          formFields.value = parseJsonToForm(tileData.value.json);
          console.log("FormFields:", formFields);
        } catch (error) {
          console.error('Failed to parse tile data:', error);
        }
      }
    });

    return {
      goBack,
      useTrigger,
      tileData,
      formFields,
      getDropdownModel,
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

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.trigger-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.service-header {
  padding: 50px 30px;
  width: 100%;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  position: relative;
  text-align: center;
  color: white;
  top: 0;
  left: 0;
}

.cancel-button {
  position: absolute;
  top: 40px;
  left: 40px;
  z-index: 10;
}

.cancel-button:hover {
  transform: scale(1.05);
}

.service-title {
  font-size: 3em;
  font-weight: bold;
  margin-bottom: 10px;
  word-wrap: break-word;
  max-width: 60%;
}

.service-source {
  font-size: 1.2em;
  margin-bottom: 10px;
  opacity: 0.8;
}

.service-description {
  font-size: 1.5em;
  margin-top: 20px;
  padding: 15px;
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  width: 80%;
  max-width: 600px;
  word-wrap: break-word;
}

.service-body {
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  width: 40%;
  max-width: 90%;
  margin-top: 20px;
  background: white;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input,
select,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.connect-button {
  width: 100%;
  padding: 15px;
  font-size: 1.2em;
  margin: 20px 0;
  border-radius: 50px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

.connect-button:hover {
  background-color: #0056b3;
}

@media (max-width: 767px) {
  .service-title {
    font-size: 2em;
    max-width: 80%;
  }

  .service-description {
    font-size: 1.2em;
    width: 90%;
  }

  .service-body {
    width: 90%;
  }
}
</style>
