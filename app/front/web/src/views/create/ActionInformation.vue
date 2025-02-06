<template>
  <router-link :to="`/action/${title.replace(/\s+/g, '-')}`" class="action-tile-link">
    <div class="action-tile" :style="{ backgroundColor: backgroundColor }">
      <h3 class="action-title">{{ title }}</h3>
      <p class="action-description">{{ description }}</p>
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
      router.push({ name: 'actionDetails', params: { id: props.id } });
    };

    return {
      goToDetails,
    };
  },
});
</script>

<style scoped>
.action-tile {
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

.action-tile:hover {
  transform: scale(1.05);
}

.action-title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
  margin-bottom: 15px;
  color: #fff;
  word-wrap: break-word;
  white-space: normal;
}

.action-description {
  margin-top: 10px;
  color: #333;
}

.action-tile-link {
  text-decoration: none;
  color: inherit;
}

.action-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 24px;
  height: 24px;
}
</style>
