<template>
  <p>Authenticating ...</p>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { queries } from '@/../lib/querier';

export default defineComponent({
  async mounted() {
    const urlParams = new URLSearchParams(window.location.href.split('?')[1]);
    const code = urlParams.get('code');
    if (code) {
      let path = "/api/v1/oauth/callback?";
      path += window.location.href.split('?')[1];
      try {
        const response = await queries.post(path);
        localStorage.setItem('authToken', response.token);
        this.$router.push('/explore/applets');
      } catch (error) {
        alert("The oauth connexion have failed.");
        this.$router.push('sign-up');
      }
    }
  }
})
</script>
