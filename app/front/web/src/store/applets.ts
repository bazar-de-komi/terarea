import { Module } from 'vuex';
import { AppState } from './index';
import { queries } from '@/../lib/querier';

export interface AppletsState {
  applets: Applet[];
  searchQuery: string;
}

export interface Applet {
  title: string;
  description: string;
  color: string;
  tags: string[];
  type: 'applet' | 'service';
}

const appletsModule: Module<AppletsState, AppState> = {
  namespaced: true,
  // state: {
  //   applets: [
  //     {
  //       title: "Update your Android wallpaper with NASA’s image of the day",
  //       description: "Change your Android wallpaper daily with NASA's image.",
  //       color: "#8140DD",
  //       tags: ['NASA', 'wallpaper', 'image', 'applet'],
  //       type: 'applet',
  //     },
  //     {
  //       title: "The Verge on YouTube integrations",
  //       description: "The Verge is a popular technology news and media network that covers a wide range of topics including gadgets, science, entertainment, and culture. They have a YouTube channel where they upload videos related to their coverage, including product reviews, interviews, and news updates. You can find their YouTube channel by searching for The Verge on YouTube.",
  //       color: '#003399',
  //       tags: ['Verge', 'news', 'technology', 'service'],
  //       type: 'service',
  //     },
  //     {
  //       title: "Ask ChatGPT anything",
  //       description: "Posez vos questions à ChatGPT pour obtenir des réponses instantanées et détaillées.",
  //       color: "#64F58C",
  //       tags: ['ChatGPT communication', 'questions', 'answers'],
  //       type: 'applet',
  //     },
  //     {
  //       title: "NASA's Astronomy Picture of the Day",
  //       description: "Affichez l'image astronomique du jour de la NASA directement sur votre écran.",
  //       color: "#8140DD",
  //       tags: ['NASA', 'astronomy', 'image', 'daily'],
  //       type: 'applet',
  //     },
  //     {
  //       title: "NASA Space News Feed",
  //       description: "Restez à jour avec les dernières nouvelles de la NASA concernant l'espace et l'astronomie.",
  //       color: "#8140DD",
  //       tags: ['NASA', 'news', 'space', 'science'],
  //       type: 'applet',
  //     },
  //     {
  //       title: "ChatGPT communication",
  //       description: "Utilisez ChatGPT pour des réponses instantanées.",
  //       color: "#64F58C",
  //       tags: ['ChatGPT', 'prompt', 'service'],
  //       type: 'service',
  //     },
  //   ],
  //   searchQuery: '',
  // },
  state: {
    applets: [],
    searchQuery: '',
  },
  mutations: {
    SET_SEARCH_QUERY(state, query: string) {
      state.searchQuery = query;
    },
    APPEND_APPLETS(state, newApplets: Applet[]) {
      state.applets = [...state.applets, ...newApplets];
    },
    CLEAR_APPLETS(state) {
      state.applets = [];
    },
  },
  getters: {
    filteredAllItems(state) {
      return state.applets.filter((applet) =>
        applet.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
        applet.description.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
        applet.tags.some(tag => tag.toLowerCase().includes(state.searchQuery.toLowerCase()))
      );
    },
    filteredServices(state) {
      return state.applets.filter((applet) =>
        applet.type === 'service' && (
          applet.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          applet.description.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          applet.tags.some(tag => tag.toLowerCase().includes(state.searchQuery.toLowerCase()))
        )
      );
    },
    filteredApplets(state) {
      return state.applets.filter((applet) =>
        applet.type === 'applet' && (
          applet.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          applet.description.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          applet.tags.some(tag => tag.toLowerCase().includes(state.searchQuery.toLowerCase()))
        )
      );
    },
  },
  actions: {
    updateSearchQuery({ commit }, query: string) {
      commit('SET_SEARCH_QUERY', query);
    },
    async updateData({ commit }) {
      try {
        const token = localStorage.getItem('authToken') || '';
        const appletsPath = '/api/v1/applets';
        const servicesPath = '/api/v1/services';

        commit('CLEAR_APPLETS');
        // const appletsResponse = await queries.get(appletsPath, {}, token);
        // for (let i = 0; i < appletsResponse.msg.length; i++) {
        //   const applets = [{
        //     title: appletsResponse.msg[i].name,
        //     description: appletsResponse.msg[i].description,
        //     color: appletsResponse.msg[i].colour,
        //     tags: appletsResponse.msg[i].tags,
        //     type: appletsResponse.msg[i].type
        //   }]
        //   commit('APPEND_APPLETS', applets);
        // }
        const servicesResponse = await queries.get(servicesPath, {}, token);
        for (let i = 0; i < servicesResponse.msg.length; i++) {
          const applets = [{
            title: servicesResponse.msg[i].name,
            description: servicesResponse.msg[i].description,
            color: servicesResponse.msg[i].colour,
            tags: servicesResponse.msg[i].tags,
            type: servicesResponse.msg[i].type
          }]
          commit('APPEND_APPLETS', applets);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des applets et services:', error);
      }
    }
  },
};

export default appletsModule;
