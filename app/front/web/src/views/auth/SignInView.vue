<template>
  <AuthLayout title="Sign In" linkText="Don't have an account? Sign up here" linkPath="/sign-up">
    <form @submit.prevent="submitSignIn">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <AuthButton text="Get started" />
    </form>
    <div class="social-login">
      <AuthButton text="Continue with Google" icon="google" />
      <AuthButton text="Continue with Apple" icon="apple" />
      <AuthButton text="Continue with Facebook" icon="facebook" />
    </div>
    <router-link to="/forgot-password">Forgot your password?</router-link>
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
    };
  },
  methods: {
    submitSignIn() {
      console.log('Sign in with', this.email, this.password);
    },
  },
});
</script>
