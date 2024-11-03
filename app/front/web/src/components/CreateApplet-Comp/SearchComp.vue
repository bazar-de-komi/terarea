<template>
  <div class="search-section">
    <input
      type="text"
      class="search-bar"
      placeholder="Search Applets or services"
      v-model="searchQuery"
      @input="updateSearchQuery"
    />
    <button class="clear-search" @click="clearSearchQuery">✖</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  setup() {
    const searchQuery = ref('');

    const updateSearchQuery = () => {
      console.log('Search Query:', searchQuery.value);
    };

    const clearSearchQuery = () => {
      searchQuery.value = '';
      updateSearchQuery();
    };

    return {
      searchQuery,
      updateSearchQuery,
      clearSearchQuery,
    };
  },
});
</script>

<style scoped>
.search-section {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.search-bar {
  width: 90%;
  max-width: 600px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 1rem;
  text-align: center;
}

.clear-search {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: -35px;
  font-size: 18px;
}
</style>
