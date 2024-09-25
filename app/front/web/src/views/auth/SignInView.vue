<template>
  <h1 class="ifttt-title">IFTTT</h1>
  <AuthLayout title="Sign In" linkText="Don't have an account? Sign up here" linkPath="/sign-up">
    <form @submit.prevent="submitSignIn" class="sign-in-form">
      <input v-model="email" type="email" placeholder="Email" required />

      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Password" required />
        <button type="button" class="toggle-password" @click="togglePassword">
          <img :src="showPassword ? showIcon : hideIcon" alt="toggle password visibility" />
        </button>
      </div>

      <AuthButton text="Get started" />
    </form>

    <div class="separator">Or</div>
    <div class="social-login">
      <AuthButton text="Continue with Google" :icon="GoogleIcon" />
      <AuthButton text="Continue with GitHub" :icon="GithubIcon" />
    </div>
    <router-link to="/forgot-password" class="forgot-password">Forgot your password?</router-link>
  </AuthLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AuthButton from '../../components/AuthButton.vue';
import AuthLayout from '../../components/AuthLayout.vue';

import showIcon from '@/assets/show.svg';
import hideIcon from '@/assets/hide.svg';
import GoogleIcon from '@/assets/googleicon.svg';
import GithubIcon from '@/assets/githubicon.svg';

export default defineComponent({
  components: {
    AuthButton,
    AuthLayout,
  },
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      showIcon,
      hideIcon,
      GoogleIcon,
      GithubIcon,
    };
  },
  methods: {
    submitSignIn() {
      console.log('Sign in with : ', this.email, this.password);
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
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

.sign-in-form input {
  display: block;
  width: 100%;
  padding: 15px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 20px;
  box-sizing: border-box;
}

.password-container {
  position: relative;
  display: flex;
  align-items: center;
}

.password-container input {
  width: 100%;
}

.toggle-password {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
}

.toggle-password img {
  height: 30px;
  width: 30px;
}

.separator {
  text-align: center;
  margin: 20px 0;
  font-size: 14px;
  position: relative;
}

.separator::before, .separator::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background-color: #000;
}

.separator::before {
  left: 0;
}

.separator::after {
  right: 0;
}

.social-login {
  margin: 20px 0;
}

.forgot-password {
  margin-top: 20px;
  color: #000;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}
</style>
