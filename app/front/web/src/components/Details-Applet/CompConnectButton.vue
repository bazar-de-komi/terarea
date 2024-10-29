<template>
  <div class="connect-button">
    <div class="circle" :style="{ backgroundColor: buttonColor }"></div>
    <span class="connect-text">Connect</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  name: 'ConnectButton',
  props: {
    buttonColor: {
      type: String as PropType<string>,
      required: true,
    },
  },
});
</script>

<style scoped>
.connect-button {
  display: flex;
  align-items: center;
  background-color: #1c1c1c;
  padding: 10px 20px;
  border-radius: 50px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  justify-content: center;
}

.circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
}

.connect-text {
  font-size: 1.7em;
  font-weight: bold;
  color: white;
}
</style>
