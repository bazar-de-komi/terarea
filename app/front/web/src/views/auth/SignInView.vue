<template>
  <img src="@/assets/logo.png" class="ifttt-logo" />
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
      <AuthButton text="Continue with Google" :buttonColor="'#f4fefe'" :textColor="'fff'" :icon="GoogleIcon" />
      <AuthButton text="Continue with GitHub" :buttonColor="'#303030'" :icon="GithubIcon" />
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
import logo from '@/assets/logo.png';

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
      logo,
    };
  },
  methods: {
    submitSignIn() {
      if (this.email === 'user@example.com' && this.password === 'password123') {
        this.$router.push('/explore/all');
      } else {
        alert('Invalid email or password');
      }
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
  },
});
</script>

<style scoped>
.ifttt-logo {
  display: block;
  margin: 0 auto 20px;
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
