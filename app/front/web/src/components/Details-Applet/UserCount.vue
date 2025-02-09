<template>
  <div class="user-count">
    <i class="fas fa-user"></i>
    <span>{{ userCount }} users</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    userCount: {
      type: Number as PropType<number>,
      required: true
    }
  }
});
</script>

<style scoped>
.user-count {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #333;
  background-color: #f5f5f5;
  border-radius: 5px;
  padding: 10px 20px;
  margin: 10px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  max-width: 200px;
}

.user-count i {
  margin-right: 10px;
  font-size: 1.5rem;
  color: #555;
}
</style>
