<template>
    <AppHeader />
    <CancelButton buttonText="Back" @click="goBack" />
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


    <button class="save-button" @click="saveChange" >Save Change</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import PasswordField from '@/views/profil/PasswordField.vue';
import { queries } from '@/../lib/querier';

export default defineComponent({
  components: {
    AppHeader,
    PasswordField,
  },
  data() {
    return {
      username: '',
      email: '',
    }
  },
  setup() {
    const router = useRouter();

    const goBack = () => {
      router.push('/explore/all');
    };

    return {
      goBack,
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("authToken") || '';
      const response = await queries.get("/api/v1/user", {}, token);

      this.username = response.msg.username;
      this.email = response.msg.email;
    } catch (error) {
      alert("Failed to retrieve your account information.");
    }
  },
  methods: {
    async saveChange() {
      try {
        const token = localStorage.getItem("authToken") || "";
        let body: { username?: string; email?: string } = {};

        if (this.username !== "") {
            body.username = this.username;
        }
        body.email = this.email;
        await queries.patch("/api/v1/user", { body }, token);
        alert("Your information was updated successfully.");
      } catch (error) {
          console.error(error);
          alert("Failed to change your information.");
      }
    }
  },
});
</script>

<style scoped>
.account-settings {
  max-width: 600px;
  margin: 200px auto 40px auto;
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
