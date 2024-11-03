<template>
  <div class="password-field">
    <label :for="id">{{ label }}</label>
    <div class="input-container">
      <input :id="id" type="password" placeholder="Can't retrieve password due to security" disabled/>
      <button @click="changePassword" class="change-password-btn">Change password</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { queries } from '@/../lib/querier';

export default defineComponent({
  props: {
    label: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      email: ''
    }
  },
  setup() {
    const router = useRouter();

    return { router };
  },
  methods: {
    async changePassword() {
      try {
          await queries.post('/api/v1/send_email_verification', {
            email: this.email
          });
          this.router.push({
            name: 'ChangePassword',
            query: { email: this.email }
          });
        } catch (error) {
          console.error('Error while sending email verification:', error);
          alert('Failed to send email verification.');
        }
    }
  },
  async mounted() {
    try {
      const token = localStorage.getItem("authToken") || '';
      const response = await queries.get("/api/v1/user", {}, token);

      this.email = response.msg.email;
    } catch (error) {
      alert("Failed to retrieve your account information.");
    }
  }
});
</script>

<style scoped>
.password-field {
  margin-bottom: 15px;
  position: relative;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

input[type="password"] {
  display: block;
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 20px;
  box-sizing: border-box;
  padding-right: 100px;
}

.change-password-btn {
  position: absolute;
  right: 15px;
  color: #007bff;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
  text-align: right;
}
</style>
