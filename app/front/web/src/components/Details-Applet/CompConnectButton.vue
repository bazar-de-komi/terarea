<template>
  <div class="connect-button">
    <div class="circle" :style="{ backgroundColor: buttonColor }"></div>
    <span class="connect-text" v-text="text" @click="onConnectOrDisconnectButton"></span>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { queries } from '@/../lib/querier';

export default defineComponent({
  name: 'ConnectButton',
  props: {
    appletId: {
      type: Number,
      required: true
    },
    buttonColor: {
      type: String as PropType<string>,
      required: true,
    },
  },
  data() {
    return {
      text: 'Connect',
    }
  },
  async mounted() {
    const token = localStorage.getItem("authToken") || '';
    try {
      const response = await queries.get("/api/v1/user_applets", {}, token);
      const userApplets = response.msg;
      for (let i = 0; i < userApplets.length; i++) {
        if (userApplets[i].id === this.appletId) {
          this.text = "Disconnect";
          return;
        }
      }
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    async onConnectOrDisconnectButton() {
      const token = localStorage.getItem("authToken") || '';
      if (this.text === "Connect") {
        try {
          let path = "/api/v1/connect_applet/";
          const idStr = this.appletId.toString();
          path += idStr;
          await queries.post(path, {}, token);
          alert("You're connected successfully to the applet.");
          this.$router.push("/explore/all");
        } catch (error) {
          alert("Failed to connect with the applet.");
        }
      } else {
        try {
          let path = "/api/v1/disconnect_applet/";
          const idStr = this.appletId.toString();
          path += idStr;
          await queries.post(path, {}, token);
          alert("You're disconnected successfully to the applet.");
          this.$router.push("/explore/all");
        } catch (error) {
          alert("Failed to disconnect with the applet.");
        }
      }
    }
  }
});
</script>

<style scoped>
.connect-button {
  display: flex;
  align-items: center;
  background-color: #1c1c1c;
  padding: 10px 20px;
  border-radius: 50px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  justify-content: center;
}

.circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
}

.connect-text {
  font-size: 1.7em;
  font-weight: bold;
  color: white;
}
</style>
