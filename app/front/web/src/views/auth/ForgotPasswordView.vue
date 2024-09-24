<template>
  <AuthLayout title="Forgot Password" linkText="Remember your password? Sign in here" linkPath="/sign-in">
    <form @submit.prevent="submitForgotPassword">
      <input v-model="email" type="email" placeholder="Email" required />
      <AuthButton text="Reset Password" />
    </form>
  </AuthLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AuthButton from '../../components/AuthButton.vue';
import AuthLayout from '../../components/AuthLayout.vue';

export default defineComponent({
  components: {
    AuthButton,
    AuthLayout,
  },
  data() {
    return {
      email: '',
    };
  },
  methods: {
    submitForgotPassword() {
      console.log('Reset password for', this.email);
    },
  },
});
</script>
