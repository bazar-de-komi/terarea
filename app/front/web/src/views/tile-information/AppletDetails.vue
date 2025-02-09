<template>
  <div>
    <header>
      <AppHeader />
      <CancelButton buttonText="Back" @click="goBack" />
    </header>

    <div v-if="!applet">Loading...</div>

    <!-- Afficher le contenu seulement si applet existe -->
    <div v-else style="margin-bottom: 30px;">
      <div class="applet-header" :style="{ backgroundColor: applet.colour }">
        <CompTitle :title="applet.name || ''" />
        <CompDescription :description="applet.description || ''" />
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
            <input v-if="field.type === 'input'" :id="field.name" type="text" :placeholder="field.placeholder" v-model="field.defaultValue">
            <textarea v-else-if="field.type === 'textarea'" :id="field.name" type="text" :placeholder="field.placeholder" v-model="field.defaultValue" />
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
            <!-- <input v-if="field.type === 'input'" :id="field.name" type="text" :placeholder="field.defaultValue" v-model="field.defaultValue">
            <textarea v-else-if="field.type === 'textarea'" :id="field.name" type="text" :placeholder="field.defaultValue" v-model="field.defaultValue" /> -->
            <div v-if="field.type === 'input' || field.type === 'textarea'" class="input-container">
              <input
                v-if="field.type === 'input'"
                :id="field.name"
                type="text"
                :placeholder="field.placeholder"
                v-model="field.defaultValue"
                ref="inputRefs"
              />
              <textarea
                v-else
                :id="field.name"
                :placeholder="field.placeholder"
                v-model="field.defaultValue"
                ref="inputRefs"
              />
              <button class="variable-button" @click="toggleVariableMenu(index, $event)">🔽</button>
            </div>
            <select v-else-if="field.type === 'dropdown'" :id="field.name" v-model="field.defaultValue">
              <option v-for="option in field.options" :key="option" :value="option">
                {{ option }}
              </option>
            </select>

            <div
              v-if="showVariableMenu === index"
              class="variable-menu"
              :style="{ top: menuPosition.top + 'px', left: menuPosition.left + 'px' }"
            >
              <button v-for="(varName, i) in availableVariables" :key="i" @click="insertVariable(index, varName)">
                ${{ varName }}
              </button>
            </div>
          </div>
        </template>
        <div class="applet-buttons-container">
          <button class="edit-button" @click="deleteApplet">✏️ Edit Applet</button>
          <button class="delete-button" @click="deleteApplet">🗑️ Delete Applet</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, onBeforeMount, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import CancelButton from '@/components/CancelButton.vue';
import CompTitle from '@/components/Details-Applet/CompTitle.vue';
import CompDescription from '@/components/Details-Applet/CompDescription.vue';
import { queries } from '@/../lib/querier';
import { parseJsonToForm, injectFormValuesIntoJson, FormField } from '@/ParseJson';

export default defineComponent({
  components: {
    AppHeader,
    CancelButton,
    CompTitle,
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

    const triggerVars = ref<Record<string, any>>({});
    const showVariableMenu = ref<number | null>(null);
    const inputRefs = ref<(HTMLInputElement | HTMLTextAreaElement)[]>([]);
    const menuPosition = ref({ top: 0, left: 0 });

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

    const toggleVariableMenu = (index: number, event: MouseEvent) => {
      if (showVariableMenu.value === index) {
        showVariableMenu.value = null;
      } else {
        showVariableMenu.value = index;
        updateMenuPosition(event);
      }
    };

    // const updateMenuPosition = (event: MouseEvent) => {
    //   nextTick(() => {
    //     const button = event.target as HTMLElement;  // Récupérer le bouton cliqué
    //     const rect = button.getBoundingClientRect();  // Obtenir la position du bouton
    //     console.log(rect);
    //     const menuHeight = 200; // Ajuste la hauteur du menu
    //     const maxHeight = window.innerHeight;
    //     const menuWidth = 200; // Ajuste la largeur du menu
    //     const maxWidth = window.innerWidth;

    //     let calculatedTop = rect.bottom + window.scrollY + 5;  // Positionner sous le bouton
    //     let calculatedLeft = rect.left + window.scrollX;  // Positionner à gauche du bouton

    //     // Si le menu dépasse le bas de l'écran, ajuster la position
    //     if (calculatedTop + menuHeight > maxHeight) {
    //       calculatedTop = maxHeight - menuHeight - 10;  // Laisser un peu d'espace
    //     }

    //     // Si le menu dépasse la droite de l'écran, ajuster la position
    //     if (calculatedLeft + menuWidth > maxWidth) {
    //       calculatedLeft = maxWidth - menuWidth - 10;  // Laisser un peu d'espace
    //     }

    //     menuPosition.value = {
    //       top: calculatedTop,
    //       left: calculatedLeft,
    //     };
    //   });
    // };

    const updateMenuPosition = (event: MouseEvent) => {
      nextTick(() => {
        const oldTopPos = (window.scrollY - window.innerHeight) + event.clientY
        let topPos = 0;
        console.log("ClientY:", event.clientY);
        console.log("Window.scrollY:", window.scrollY);
        console.log("Inner height:", window.innerHeight);
        if (window.scrollY > window.innerHeight) {
          console.log("After calcul:", window.scrollY - event.clientY - window.innerHeight);
          topPos = (window.scrollY - window.innerHeight) + event.clientY;
        } else {
          console.log("After calcul:", window.scrollY - event.clientY + window.innerHeight);
          topPos = (window.scrollY - window.innerHeight) + event.clientY + 410;
        }
        menuPosition.value = {
          top: topPos,
          left: window.innerWidth - event.clientX,
        };
      });
    };

    // const updateMenuPosition = (event: MouseEvent) => {
    //   nextTick(() => {
    //     const menuHeight = 200; // Ajuste la hauteur du menu si nécessaire
    //     const maxHeight = window.innerHeight;

    //     let calculatedTop = event.clientY + window.scrollY + 5;

    //     // Si le menu dépasse le bas de l'écran, ajuster la position
    //     if (calculatedTop + menuHeight > maxHeight) {
    //       calculatedTop = maxHeight - menuHeight - 10; // Laisser un peu d'espace
    //     }

    //     menuPosition.value = {
    //       top: calculatedTop,
    //       left: event.clientX + window.scrollX,
    //     };
    //   });
    // };

    // const updateMenuPosition = (event: MouseEvent) => {
    //   nextTick(() => {
    //     menuPosition.value = {
    //       top: event.clientY + 10,  // Ajustement
    //       left: event.clientX,      // Ajustement
    //     };
    //   });
    // };

    // const updateMenuPosition = (event: MouseEvent) => {
    //   nextTick(() => {
    //     const menuWidth = 200; // Largeur du menu (à ajuster en fonction de ta taille)
    //     const menuHeight = 150; // Hauteur du menu (ajustée aussi si nécessaire)

    //     const pageWidth = window.innerWidth;
    //     const pageHeight = window.innerHeight;

    //     // Calcul de la position à gauche et en haut avec des ajustements pour éviter que le menu sorte de la fenêtre
    //     const leftPosition = event.clientX + window.scrollX - 300;
    //     const topPosition = event.clientY + window.scrollY + 5; // Position sous le bouton
      
    //     menuPosition.value = {
    //       left: leftPosition + menuWidth > pageWidth ? pageWidth - menuWidth - 10 : leftPosition, // Ajuste si ça dépasse la droite
    //       top: topPosition + menuHeight > pageHeight ? pageHeight - menuHeight - 10 : topPosition, // Ajuste si ça dépasse le bas
    //     };
    //   });
    // };

    const insertVariable = (index: number, variable: string) => {
      const inputElement = inputRefs.value[index];
      console.log(inputElement);
      if (inputElement) {
        const start = inputElement.selectionStart || 0;
        const end = inputElement.selectionEnd || 0;
        const value = reactionFormFields.value[index].defaultValue || "";

        const formattedVariable = `\${{${variable}}}`;

        reactionFormFields.value[index].defaultValue =
          value.substring(0, start) + formattedVariable + value.substring(end);

        nextTick(() => {
          inputElement.focus();
          inputElement.setSelectionRange(start + formattedVariable.length, start + formattedVariable.length);
        });
      }

      showVariableMenu.value = null;
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
            triggerVars.value = applet.value.trigger.service["ignore:vars"];
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
      showVariableMenu,
      toggleVariableMenu,
      insertVariable,
      inputRefs,
      menuPosition,
      availableVariables: computed(() => Object.keys(triggerVars.value)),
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

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.input-container {
  display: flex;
  align-items: center;
  position: relative;
}

.variable-button {
  margin-left: 5px;
  padding: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.variable-menu {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 100;
  width: 200px;
  display: flex;
  flex-direction: column;
}

.variable-menu button {
  padding: 10px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
}

.variable-menu button:hover {
  background-color: #f0f0f0;
}

.edit-button {
  background-color: #4ea8de;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  margin-right: 30px;
  transition: 0.3s;
}

.edit-button:hover {
  background-color: #0077b6;
  transform: scale(1.05);
}

.delete-button {
  background-color: rgba(255, 38, 0, 0.767);
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
</style>
