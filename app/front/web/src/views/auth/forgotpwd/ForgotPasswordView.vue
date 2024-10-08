<template>
  <img src="@/assets/logo.png" class="ifttt-logo" />
  <AuthLayout title="Forgot Password" linkText="Remember your password? Sign in here" linkPath="/sign-in">
    <form @submit.prevent="submitForgotPassword" class="forgot-password-form">
      <input v-model="email" type="email" placeholder="Email" required />
      <AuthButton text="Reset Password" />
    </form>
  </AuthLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AuthButton from '../../../components/AuthButton.vue';
import AuthLayout from '../../../components/AuthLayout.vue';
import { useRouter } from 'vue-router';

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
  setup() {
    const router = useRouter();

    return {
      router,
    };
  },
  methods: {
    submitForgotPassword() {
      if (this.email) {
        console.log('Reset password for', this.email);
        this.router.push({
          name: 'ResetPassword',
          query: { email: this.email }
        });
      }
    },
  },
});
</script>

<style scoped>
.ifttt-logo {
  display: block;
  margin: 0 auto 20px;
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
