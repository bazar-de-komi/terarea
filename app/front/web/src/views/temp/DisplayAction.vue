<template>
  <div class="choose-service-page">
    <header class="header">
      <CancelButton buttonText="Back" @click="goBack" class="cancel-button" />
      <h1 class="page-title">Choose a Service</h1>
    </header>

    <div class="search-section">
      <input
        type="text"
        class="search-bar"
        placeholder="Search Action"
        v-model="searchQuery"
      />
      <button class="clear-search" @click="clearSearchQuery">✖</button>
    </div>

    <!-- Divider -->
    <div class="divider"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import CancelButton from '@/components/CancelButton.vue';

export default defineComponent({
  components: {
    CancelButton,
  },
  setup() {
    const router = useRouter();
    const searchQuery = ref('');

    const goBack = () => {
      router.push('/explore/all');
    };

    const clearSearchQuery = () => {
      searchQuery.value = '';
    };

    return {
      searchQuery,
      goBack,
      clearSearchQuery,
    };
  },
});
</script>

<style scoped>
.choose-service-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 20px;
}

.cancel-button {
  margin-top: -80px;
  margin-right: auto;
}

.page-title {
  margin: 0 auto;
  font-size: 2rem;
  font-weight: bold;
}

.search-section {
  display: flex;
  align-items: center;
  margin-top: 80px;
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-bar {
  width: 100%;
  padding: 15px 20px;
  font-size: 1.1rem;
  border: 2px solid #ccc;
  border-radius: 25px;
  outline: none;
  text-align: center;
}

.search-bar:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.25);
}

.clear-search {
  position: absolute;
  right: 15px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.divider {
  margin: 50px auto;
  width: 80%;
  height: 4px;
  background-color: #ddd;
  border-radius: 2px;
}
</style>
