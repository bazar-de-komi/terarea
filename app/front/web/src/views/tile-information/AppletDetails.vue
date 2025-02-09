<template>
  <div>
    <header>
      <AppHeader />
      <CancelButton buttonText="Back" @click="goBack" />
    </header>

    <div v-if="!applet">Loading...</div>

    <!-- Afficher le contenu seulement si applet existe -->
    <div v-else>
      <div class="applet-header" :style="{ backgroundColor: applet.colour }">
        <CompTitle :title="applet.name || ''" />
        <CompDescription :description="applet.description || ''" />
        <button class="delete-button" @click="deleteApplet">🗑️ Delete Applet</button>
      </div>

      <div class="applet-body" :style="{ backgroundColor: applet.colour }">
        <h2>Basic applet informations</h2>
          <div class="basic-form-group">
            <label>Your applet name</label>
            <input v-model="applet_name" placeholder="Enter applet name" />

            <label>Your applet description</label>
            <input v-model="applet_description" placeholder="Enter applet description" />

            <label>Your applet tags (Optional)</label>
            <input v-model="applet_tags" placeholder="Enter tags" />

            <label>Your applet colour</label>
            <input type="color" v-model="applet_colour" />
          </div>

        <h2>Trigger: {{applet.trigger.name}}</h2>
        <template v-if="triggerFormFields.length">
          <div v-for="(field, index) in triggerFormFields" :key="index" class="form-group">
            <label :for="field.name">{{ field.name }}</label>
            <input v-if="field.type === 'input'" :id="field.name" type="text" :placeholder="field.defaultValue" v-model="field.defaultValue">
            <textarea v-else-if="field.type === 'textarea'" :id="field.name" type="text" :placeholder="field.defaultValue" v-model="field.defaultValue" />
            <select v-else-if="field.type === 'dropdown'" :id="field.name" v-model="field.defaultValue">
              <option v-for="option in field.options" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>
        </template>
        <div class="separate-form-group"></div>

        <h2>Reaction: {{applet.consequences.name}}</h2>
        <template v-if="triggerFormFields.length">
          <div v-for="(field, index) in reactionFormFields" :key="index" class="form-group">
            <label :for="field.name">{{ field.name }}</label>
            <input v-if="field.type === 'input'" :id="field.name" type="text" :placeholder="field.defaultValue" v-model="field.defaultValue">
            <textarea v-else-if="field.type === 'textarea'" :id="field.name" type="text" :placeholder="field.defaultValue" v-model="field.defaultValue" />
            <select v-else-if="field.type === 'dropdown'" :id="field.name" v-model="field.defaultValue">
              <option v-for="option in field.options" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import CancelButton from '@/components/CancelButton.vue';
import CompTitle from '@/components/Details-Applet/CompTitle.vue';
// import CompConnectButton from '@/components/Details-Applet/CompConnectButton.vue';
import CompDescription from '@/components/Details-Applet/CompDescription.vue';
import { queries } from '@/../lib/querier';
import { parseJsonToForm, injectFormValuesIntoJson, FormField } from '@/ParseJson';

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    CompTitle,
    // CompConnectButton,
    CompDescription,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const applet = ref<any>(null);
    const triggerFormFields = ref<FormField[]>([]);
    const reactionFormFields = ref<FormField[]>([]);
    const applet_name = ref('');
    const applet_description = ref('');
    const applet_tags = ref('');
    const applet_colour = ref('');

    const appletId = computed(() => {
      const title = Array.isArray(route.params.title) ? route.params.title[0] : route.params.title;
      return title ? title.split('-')[0] : null;
    });

    const goBack = () => {
      router.back();
    };

    const deleteApplet = async () => {
    if (!applet.value) return;

    const confirmDelete = confirm(`Do you really want to delete "${applet.value.name}" ?`);
    if (!confirmDelete) return;

    try {
      const token = localStorage.getItem("authToken") || "";
      const response = await queries.delete_query(`/api/v1/my_applet/${applet.value.id}`, {}, token);

      if (response.resp === "success") {
        alert("Applet deleted successfully !");
        router.back();
      } else {
        alert("Error encountered while deleting applet !");
      }
    } catch (error) {
      console.error("Erreur lors de la suppression :", error);
      alert("Error encountered while deleting applet !");
    }
  };

    onBeforeMount(async () => {
      if (appletId.value) {
        try {
          const token = localStorage.getItem("authToken") || "";
          const response = await queries.get(`/api/v1/my_applet/${appletId.value}`, {}, token);
          if (response.resp === "success") {
            applet.value = response.msg;
            applet_name.value = applet.value.name;
            applet_description.value = applet.value.description;
            applet_tags.value = applet.value.tags;
            applet_colour.value = applet.value.colour;
            triggerFormFields.value = parseJsonToForm(applet.value.trigger);
            reactionFormFields.value = parseJsonToForm(applet.value.consequences);
          }
        } catch (error) {
          console.error(error)
        }
      }
    })

    return {
      applet,
      goBack,
      deleteApplet,
      triggerFormFields,
      reactionFormFields,
      applet_name,
      applet_description,
      applet_tags,
      applet_colour,
    };
  }
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

h2 {
  color: white;
}

.applet-header {
  padding: 50px 30px;
  width: 100%;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  z-index: 1;
  top: 0;
  left: 0;
  right: 0;
  position: absolute;
  height: auto;
}

.cancel-button {
  color: white;
  background-color: black;
  z-index: 3;
}

.cancel-button:hover {
  background-color: #212121;
  transform: scale(1.05);
}

.applet-title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
  word-wrap: break-word;
  max-width: 40%;
  line-height: 1.2;
}

.applet-source {
  font-size: 1.2em;
  margin-bottom: 10px;
  text-align: center;
}

.applet-stats {
  font-size: 1em;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 0;
}

.applet-body {
  position: relative;
  top: 500px;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  z-index: 2;
  width: 40%;
  max-width: 90%;
  margin: 0 auto;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  height: auto;
}

.connect-button {
  width: 100%;
  padding: 15px;
  font-size: 1.2em;
  margin: 20px 0;
  border-radius: 50px;
  text-align: center;
}

.applet-description {
  font-size: 1.5em;
  margin-top: 20px;
  text-align: center;
  padding: 15px;
  color: white;
  font-weight: bold;
  background-color: transparent;
  border-radius: 10px;
  width: auto;
  max-width: 90%;
  word-wrap: break-word;
}

.delete-button {
  background-color: red;
  color: white;
  border: none;
  font-weight: bold;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 20px;
  transition: 0.3s;
}

.delete-button:hover {
  background-color: darkred;
  transform: scale(1.05);
}

.basic-form-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 15px;
}

.basic-form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  display: block;
  margin: 10px 0 5px;
  text-align: left;
  width: 100%;
}

.basic-form-group input {
  width: 100%;
  /* max-width: 600px; */
  padding: 12px;
  font-size: 1rem;
  border: 2px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s ease;
}

.basic-form-group input:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.2);
}

.basic-form-group input[type="color"] {
  width: 60px;
  height: 40px;
  padding: 5px;
  border: none;
  cursor: pointer;
  margin-bottom: 40px;
}

.separate-form-group {
  margin-bottom: 25px;
}

.form-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  color: white;
  margin-bottom: 5px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>

