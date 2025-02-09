<template>
  <AppHeader />
  <CancelButton ButtonText="Back" @click="goBack" />
  <AuthLayout title="Change Password" link-text="" link-path="">
    <form @submit.prevent="submitPasswordReset" class="forgot-password-form">
      <input v-model="verificationCode" type="text" placeholder="Verification code" required />
      <button @click.prevent="resendVerificationEmail" class="resend-email-btn">Resend verification email</button>
      <div class="password-container">
        <input :type="showPassword ? 'text' : 'password'" v-model="newPassword" placeholder="New Password" required />
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
import { useRoute, useRouter } from 'vue-router';
import AuthButton from '@/components/AuthButton.vue';
import AuthLayout from '@/views/profil/ChangeLayout.vue';
import AppHeader from '@/components/AppHeader.vue';
import CancelButton from '@/components/CancelButton.vue'
import { queries } from '@/../lib/querier';

import showIcon from '@/assets/show.svg';
import hideIcon from '@/assets/hide.svg';

export default defineComponent({
  components: {
    AuthButton,
    AuthLayout,
    AppHeader,
    CancelButton,
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
    const router = useRouter();
    const route = useRoute();

    const goBack = () => {
      router.back();
    };

    return {
      route,
      goBack,
    };
  },
  methods: {
    async submitPasswordReset() {
      if (this.newPassword !== this.passwordConfirmation) {
        alert('Passwords do not match!');
        return;
      }
      try {
        await queries.patch("/api/v1/reset_password", {
          code: this.verificationCode,
          email: this.email,
          password: this.newPassword
        })
        this.$router.push('/account');
      } catch (error) {
        console.error(error);
        alert("Failed to change the password.");
      }
    },
    async resendVerificationEmail() {
      await queries.post("/api/v1/send_email_verification", {
        email: this.email
      })
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
  },
});
</script>

<style scoped>
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
