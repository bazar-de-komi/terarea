<template>
  <router-link :to="`/service/${title.replace(/\s+/g, '-')}`" class="service-tile-link">
    <div class="service-tile" :style="{ backgroundColor: backgroundColor }">
      <img v-if="icon" :src="icon" class="service-icon" alt="icon" />
      <h3 class="service-title">{{ title }}</h3>
      <p class="service-description">{{ description }}</p>
    </div>
  </router-link>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  props: {
    id: Number,
    title: String,
    description: String,
    backgroundColor: String,
    icon: String,
  },
  setup(props) {
    const router = useRouter();

    const goToDetails = () => {
      router.push({ name: 'ServiceDetails', params: { id: props.id } });
    };

    return {
      goToDetails,
    };
  },
});
</script>

<style scoped>
.service-tile {
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  position: relative;
  width: 250px;
  height: 300px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.service-tile:hover {
  transform: scale(1.05);
}

.service-title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
  margin-bottom: 15px;
  color: #fff;
  word-wrap: break-word;
  white-space: normal;
}

.service-description {
  margin-top: 10px;
  color: #333;
}

.service-tile-link {
  text-decoration: none;
  color: inherit;
}

.service-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 24px;
  height: 24px;
}
</style>
