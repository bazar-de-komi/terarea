<template>
  <div class="applet-stats">
    <span class="users-count">{{ userCount }} users</span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    userCount: {
      type: Number,
      required: true,
    },
  },
});
</script>

<style scoped>
.applet-stats {
  margin: 15px 0;
}

.users-count {
  background-color: #333;
  color: white;
  padding: 10px 20px;
  border-radius: 15px;
  font-size: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
