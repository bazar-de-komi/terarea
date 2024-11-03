<template>
  <div class="ifThenContainer">
    <div class="ifThenBlock">
      <span>If</span>
      <AddButton
        v-if="!serviceSelectedIf"
        @click="addServiceIf"
        :route="'/create/add-action'"
        class="add-button-right"
      />
      <span v-else>{{ serviceSelectedIf }}</span>
    </div>
    <div class="ifThenBlock">
      <span>Then</span>
      <AddButton
        v-if="showAddButton && !serviceSelectedThen"
        @click="addServiceThen"
        :route="'/create/add-reaction'"
        class="add-button-right"
      />
      <span v-else>{{ serviceSelectedThen }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AddButton from '@/components/CreateApplet-Comp/AddDelButtonComp.vue';

export default defineComponent({
  components: {
    AddButton,
  },
  props: {
    serviceSelectedIf: {
      type: String,
      default: '',
    },
    serviceSelectedThen: {
      type: String,
      default: '',
    },
    showAddButton: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['add-service-if', 'add-service-then'],
  methods: {
    addServiceIf() {
      this.$emit('add-service-if');
    },
    addServiceThen() {
      this.$emit('add-service-then');
    },
  },
});
</script>

<style scoped>
.ifThenContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
  padding: 20px;
  min-height: 60vh;
  box-sizing: border-box;
  gap: 20px; /* Espacement entre les blocs If et Then */
}

.ifThenBlock {
  background-color: black;
  color: white;
  padding: 20px;
  border-radius: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 800px; /* Taille fixe de 800px */
  text-align: center;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.ifThenBlock:nth-child(2) {
  background-color: grey; /* Fond gris pour Then That */
}

.ifThenBlock span {
  font-weight: bold;
  font-size: 24px; /* Taille fixe du texte */
  white-space: nowrap;
  flex-grow: 1;
  text-align: center;
}

.add-button-right {
  position: absolute;
  right: 15px; /* Alignement du bouton */
}
</style>
