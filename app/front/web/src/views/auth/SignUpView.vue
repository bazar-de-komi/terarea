<template>
  <AuthLayout title="Sign Up" linkText="Already have an account? Sign in here" linkPath="/sign-in">
    <form @submit.prevent="submitSignUp">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
      <AuthButton text="Get started" />
    </form>
    <div class="social-login">
      <AuthButton text="Continue with Google" icon="google" />
      <AuthButton text="Continue with Apple" icon="apple" />
      <AuthButton text="Continue with Facebook" icon="facebook" />
    </div>
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
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    submitSignUp() {
      console.log('Sign up with', this.email, this.password, this.confirmPassword);
    },
  },
});
</script>
