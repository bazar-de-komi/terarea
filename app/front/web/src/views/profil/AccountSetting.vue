<template>
    <AppHeader />
    <BackButton ButtonText="Back" @click="goBack" />
  <div class="account-settings">

    <h1>Account Settings</h1>

    <div class="profile-section">
        <img src="@/assets/profile-icon.svg" alt="Profile" class="profile-icon" />
    </div>

    <div class="form-section">
      <label for="username">Username</label>
      <input id="username" type="text" v-model="username" class="text-input" />
    </div>

    <div class="form-section">
      <label for="email">Email</label>
      <input id="email" type="email" v-model="email" class="text-input" />
    </div>

    <div class="form-section">
      <PasswordField label="Password" id="password" />
    </div>


    <Button text="Save Change" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import BackButton from '@/components/CancelButton.vue';
import Button from '@/components/AuthButton.vue'
import PasswordField from '@/views/profil/PasswordField.vue';

export default defineComponent({
  components: {
    AppHeader,
    BackButton,
    PasswordField,
    Button,
  },
  setup() {
    const router = useRouter();
    const goBack = () => {
      router.push('/explore/all');
    };

    const username = ref('totolebouc91');
    const email = ref('toto.lebouc91@gmail.com');

    return {
      goBack,
      username,
      email,
    };
  },
});
</script>

<style scoped>
.account-settings {
  max-width: 600px;
  margin: 60px auto;
  padding: 40px;
  background-color: #f5f5f5;
  border-radius: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.profile-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  margin-bottom: 10px;
}

.icon-placeholder {
  color: #666;
}

.link-button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 14px;
}

.link-button:hover {
  text-decoration: underline;
}

.form-section {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  font-weight: bold;
  color: #333;
  margin-bottom: 6px;
}

.text-input {
  display: block;
  width: 100%;
  padding: 15px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 20px;
  box-sizing: border-box;
}

.text-input:focus {
  border-color: #007bff;
}

.save-button {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background-color: #999;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #bbb;
}
</style>
