<template>
  <p class="service-description">{{ description }}</p>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    description: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped>
.service-description {
  color: #ccc;
  font-size: 1.1rem;
  margin-top: 15px;
  max-width: 700px;
  text-align: center;
}
</style>
