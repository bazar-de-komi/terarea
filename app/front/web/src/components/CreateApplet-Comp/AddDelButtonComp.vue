<template>
  <button class="add-button" @click="navigate">
    {{ label }}
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  props: {
    label: {
      type: String,
      default: 'Add',
    },
    route: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();

    const navigate = () => {
      if (props.route) {
        router.push(props.route);
      }
    };

    return {
      navigate,
    };
  },
});
</script>

<style scoped>
.add-button {
  background-color: white;
  color: black;
  border-radius: 15px; /* Légèrement réduit */
  padding: 0.5vw 1vw; /* Ajusté pour un meilleur rendu */
  font-size: 1.5vw; /* Adapté pour mieux correspondre */
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background-color: #e0e0e0;
}
</style>
