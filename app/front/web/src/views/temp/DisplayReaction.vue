<template>
  <div class="explore-page">
    <CancelButton ButtonText="Back" @click="goBack" />
    <header class="page-header">
      <h1 class="page-title">Choose a Service</h1>
    </header>
    <SearchComponent />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import CancelButton from '@/components/CancelButton.vue';
import SearchComponent from '@/views/temp/SearchComp.vue';

export default defineComponent({
  components: {
    CancelButton,
    SearchComponent,
  },
  setup() {
    const router = useRouter();

    const goBack = () => {
      router.push('/create');
    };

    return {
      goBack,
    };
  },
});
</script>

<style scoped>
.explore-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.page-header {
  width: 100%;
  text-align: center;
  margin-top: 20px;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}
</style>
