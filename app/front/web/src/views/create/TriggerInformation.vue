<template>
  <div class="trigger-page">
    <header>
      <CancelButton buttonText="Back" @click="goBack" class="cancel-button" />
    </header>

    <div class="service-header" :style="{ backgroundColor: tileData?.backgroundColor }">
      <h1 class="service-title">{{ tileData?.title }}</h1>
      <p class="service-source">{{ tileData?.name }}</p>
      <p class="service-description">{{ tileData?.description }}</p>
    </div>

    <div class="service-body">
      <button class="connect-button" @click="useTrigger">Use this Trigger</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import CancelButton from '@/components/CancelButton.vue';

export default defineComponent({
  components: {
    CancelButton,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const tileData = ref<any>(null);

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

    onMounted(() => {
      if (route.query.tile) {
        try {
          tileData.value = JSON.parse(route.query.tile as string);
        } catch (error) {
          console.error('Failed to parse tile data:', error);
        }
      }
    });

    return {
      goBack,
      useTrigger,
      tileData,
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
}

.cancel-button {
  position: absolute;
  top: 20px;
  left: 20px;
  background-color: black;
  color: white;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #212121;
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
  margin-top: -50px;
  background: white;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
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
