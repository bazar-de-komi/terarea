<template>
  <div class="block-details" :style="{ width: `${blockWidth}px` }">
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>

    <div v-for="(field, index) in parsedFields" :key="index" class="field">
      <template v-if="field.type === 'Dropdown'">
        <label>{{ field.name }}:</label>
        <select v-model="field.value">
          <option v-for="option in field.options" :key="option" :value="option">{{ option }}</option>
        </select>
      </template>

      <template v-else-if="field.type === 'Date'">
        <label>{{ field.name }}:</label>
        <input type="date" v-model="field.value" />
      </template>

      <template v-else-if="field.type === 'Time'">
        <label>{{ field.name }}:</label>
        <input type="time" v-model="field.value" />
      </template>

      <template v-else-if="field.type === 'Input'">
        <label>{{ field.name }}:</label>
        <input type="text" v-model="field.value" />
      </template>

      <template v-else-if="field.type === 'Textarea'">
        <label>{{ field.name }}:</label>
        <textarea v-model="field.value"></textarea>
      </template>

      <template v-else-if="field.type === 'int'">
        <label>{{ field.name }}:</label>
        <input type="number" v-model="field.value" :min="field.min" :max="field.max" />
      </template>

      <template v-else-if="field.type === 'email'">
        <label>{{ field.name }}:</label>
        <input type="email" v-model="field.value" />
      </template>

      <template v-else-if="field.type === 'tel'">
        <label>{{ field.name }}:</label>
        <input type="tel" v-model="field.value" />
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from 'vue';

interface Field {
  type: string;
  name: string;
  value?: any;
  options?: string[];
  min?: number;
  max?: number;
}

export default defineComponent({
  name: 'BlockDetails',
  props: {
    title: String,
    description: String,
    fieldsData: {
      type: Array as PropType<string[]>,
      required: true,
    },
    blockWidth: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const parseFields = (fieldsData: string[]): Field[] => {
      return fieldsData.map((data) => {
        const [type, name] = data.split(':');
        const field: Field = { type, name };

        if (type.toLowerCase() === 'dropdown') {
          field.options = ['Option 1', 'Option 2'];
          field.value = 'Option 1';
        } else if (type.toLowerCase() === 'int') {
          field.min = 0;
          field.max = 100;
          field.value = field.min;
        } else if (type.toLowerCase() === 'date' || type.toLowerCase() === 'time') {
          field.value = new Date().toISOString().split('T')[0];
        }

        return field;
      });
    };

    const parsedFields = computed(() => parseFields(props.fieldsData));

    return {
      parsedFields,
    };
  },
});
</script>

<style scoped>
.block-details {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transition: height 0.3s ease;
}

.field {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
