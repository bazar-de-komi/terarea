<template>
  <button class="auth-button" :style="{ backgroundColor: buttonColor, color: textColor }" @click="onClick">
    <img v-if="icon" :src="icon" alt="icon" class="auth-icon" />
    <span>{{ text }}</span>
  </button>
</template>

<script lang="ts">
import { defineComponent, shallowRef } from 'vue';
import { queries } from '@/../lib/querier';

export default defineComponent({
  props: {
    text: { type: String, required: true },
    icon: { type: String, required: false },
    buttonColor: { type: String, required: false, default: '#666' },
    textColor: { type: String, required: false, default: '#fff' },
    provider: { type: String, required: false }
  },
  data() {
    return {
      popup: shallowRef<Window | null>(null),
    };
  },
  methods: {
    // watchPopup() {
    //   if (this.popup && !this.popup.closed) {
    //     try {
    //       let currentURL = this.popup.location.href;
    //       console.log("URL actuelle de la popup:", currentURL);
    //     } catch (error) {
    //       console.log("Impossible d'accéder a la popup.");
    //     }
    //     setTimeout(this.watchPopup, 1000);
    //   } else {
    //     console.log("Popup fermée.");
    //   }
    // },

    async onClick() {
      if (this.provider) {
        // const width = 500;
        // const height = 600;
        // const left = (window.innerWidth - width) / 2;
        // const top = (window.innerHeight - height) / 2;
        // const providerData = {
        //   provider: this.provider
        // }

        const response = await queries.post("/api/v1/oauth/login", {
          provider: this.provider
        });
        let url: string = response.authorization_url;
        url = decodeURIComponent(url);
        window.location.href = url;
        // this.popup = window.open(
        //   url,
        //   "OAuth2 Authorization",
        //   `width=${width},height=${height},top=${top},left=${left}`
        // );
        // this.watchPopup();
        // window.addEventListener("message", (event) => {
        //   console.log("Inside event listener");
        //   if (event.origin === "https://accounts.google.com") {
        //     // if (event.origin === "http://localhost:8080") {
        //     console.log("Inside inside event listener");
        //     const authorizationCode = event.data.code;
        //     window.location.href = "http://localhost:8080/sign-up";
        //     // popup?.close();
        //     // console.log("Code d'autorisation reçu :", authorizationCode);
        //     // // Vous pouvez maintenant échanger le code d'autorisation contre un token
        //   }
        // })
        // window.addEventListener("message", (event) => {
        //   console.log("Popup1");
        //   if (event.origin === "https://accounts.google.com") { // Assurez-vous de bien spécifier l'URL
        //     console.log("Popup2");
        //     // const authorizationCode = event.data.code;
        //     // console.log("Code d'autorisation reçu :", authorizationCode);
        //     // window.location.href = "http://localhost:8080/sign-up";
        //   }
        // });
      }
    },
  }
});
</script>

<style scoped>
.auth-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 22.5px;
  margin-top: 15px;
  border: none;
  border-radius: 75px;
  font-size: 27px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s ease-in-out;
}

.auth-button:hover {
  background-color: #999;
}

.auth-button:active {
  background-color: #bbb;
  transform: scale(0.98);
}

.auth-icon {
  margin-right: 15px;
  height: 50px;
  width: 50px;
}
</style>
