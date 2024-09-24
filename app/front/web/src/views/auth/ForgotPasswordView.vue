<template>
  <h1 class="ifttt-title">IFTTT</h1>
  <AuthLayout title="Forgot Password" linkText="Remember your password? Sign in here" linkPath="/sign-in">
    <form @submit.prevent="submitForgotPassword" class="forgot-password-form">
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

<style scoped>
.ifttt-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 50px;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
}

.forgot-password-form input {
  display: block;
  width: 100%;
  padding: 15px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 20px;
  box-sizing: border-box;
}

.forgot-password-form button {
  margin-top: 10px;
}
</style>
