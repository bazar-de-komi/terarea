<template>
  <div class="container">
    <div class="ifThisBlock">
      <span>If This</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    action: {
      type: Object as PropType<{ name: string; description: string; logo: string; color: string } | null>,
      required: false
    }
  },
  computed: {
    serviceColor(): string {
      return this.action && this.action.color ? this.action.color : 'default-gray';
    }
  },
  methods: {
    addService() {
      this.$emit('service-selected', {
        name: 'Service ABC',
        description: 'Send a notification',
        logo: '/path/to/logo.png',
        color: 'service-green'
      });
    },
    editService() {
      alert('Edit service');
    },
    deleteService() {
      this.$emit('service-selected', null);
    }
  }
});
</script>

<style scoped>
.then-block {
  background-color: black;
  color: white;
  padding: 10px 5vw;
  border-radius: 75px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5vw;
  max-width: 90%;
  flex-wrap: wrap;
  text-align: center;
  font-family: Arial, sans-serif;
}

.then-block button {
  background-color: white;
  color: black;
  border-radius: 20px;
  padding: 1vw 1vw;
  font-size: 20px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}

.default-gray {
  background-color: #ccc;
}

.service-green {
  background-color: #4caf50;
}

@media (max-width: 600px) {
  .then-block {
    padding: 8px 3vw;
    gap: 1vw;
  }

  .then-block h3 {
    font-size: 6vw;
  }

  .then-block button {
    padding: 2vw 4vw;
    font-size: 4vw;
  }

}
</style>
