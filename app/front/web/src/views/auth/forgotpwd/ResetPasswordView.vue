<template>
  <img src="@/assets/logo.png" class="ifttt-logo" />
  <AuthLayout title="Reset Password" link-text="" link-path="">
    <form @submit.prevent="submitPasswordReset" class="forgot-password-form">
      <button @click.prevent="resendVerificationEmail" class="resend-email-btn">Resend verification email</button>
      <input v-model="verificationCode" type="text" placeholder="Verification code" required />
      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="newPassword" placeholder="Password" required />
        <button type="button" class="toggle-password" @click="togglePassword">
          <img :src="showPassword ? showIcon : hideIcon" alt="toggle password visibility" />
        </button>
      </div>
      <div class="password-container">
        <input :type="showConfirmPassword ? 'text' : 'password'" v-model="passwordConfirmation" placeholder="Password confirmation" required />
        <button type="button" class="toggle-password" @click="toggleConfirmPassword">
          <img :src="showConfirmPassword ? showIcon : hideIcon" alt="toggle password visibility" />
        </button>
      </div>
      <AuthButton text="Set password" />
    </form>
  </AuthLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AuthButton from '../../../components/AuthButton.vue';
import AuthLayout from '../../../components/AuthLayout.vue';
import { useRoute } from 'vue-router';

import showIcon from '@/assets/show.svg';
import hideIcon from '@/assets/hide.svg';

export default defineComponent({
  components: {
    AuthButton,
    AuthLayout,
  },
  data() {
    return {
      email: '',
      verificationCode: '',
      newPassword: '',
      passwordConfirmation: '',
      showPassword: false,
      showConfirmPassword: false,
      showIcon,
      hideIcon,
    };
  },
  setup() {
    const route = useRoute();

    return {
      route,
    };
  },
  methods: {
    submitPasswordReset() {
      if (this.newPassword !== this.passwordConfirmation) {
        alert('Passwords do not match!');
        return;
      }

      console.log('Resetting password for', this.email);
      console.log('Verification Code:', this.verificationCode);
      console.log('New Password:', this.newPassword);
    },
    resendVerificationEmail() {
      console.log('Resending verification email to', this.email);
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
  },
  mounted() {
    this.email = this.route.query.email as string;
    console.log('Received email:', this.email);
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

.password-container {
  position: relative;
  display: flex;
  align-items: center;
}

.resend-email-btn {
  display: block;
  margin-bottom: 15px;
  background-color: #6c63ff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.resend-email-btn:hover {
  background-color: #5753c9;
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
</style>
