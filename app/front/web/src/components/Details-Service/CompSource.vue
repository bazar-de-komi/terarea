<template>
  <p class="service-source">by {{ source }}</p>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    source: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped>
.service-source {
  font-size: 1.1rem;
  color: #ccc;
  margin-bottom: 10px;
}
</style>
