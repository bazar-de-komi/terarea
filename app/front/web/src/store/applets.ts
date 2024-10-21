import { Module } from 'vuex';
import { AppState } from './index';

export interface AppletsState {
  applets: Applet[];
  searchQuery: string;
}

export interface Applet {
  title: string;
  description: string;
  color: string;
  tags: string[];
}

const appletsModule: Module<AppletsState, AppState> = {
  namespaced: true,
  state: {
    applets: [
      {
        title: "Update your Android wallpaper with NASA’s image of the day",
        description: "Change your Android wallpaper daily with NASA's image.",
        color: "#8140DD",
        tags: ['NASA', 'wallpaper', 'image', 'applet'],
      },
      {
        title: "Get the weather forecast every day at 7:00 am",
        description: "Receive daily weather forecasts.",
        color: "#FF6347",
        tags: ['weather', 'forecast', 'daily', 'applet'],
      },
      {
        title: "on fait des teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest",
        description: "Receive daily weather forecasts.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        color: "#FF6347",
        tags: ['test', 'forecast', 'service'],
      },
    ],
    searchQuery: '',
  },
  mutations: {
    SET_SEARCH_QUERY(state, query: string) {
      state.searchQuery = query;
    },
  },
  getters: {
    filteredApplets(state) {
      return state.applets.filter((applet) =>
        applet.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
        applet.description.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
        applet.tags.some(tag => tag.toLowerCase().includes(state.searchQuery.toLowerCase()))
      );
    },
  },
  actions: {
    updateSearchQuery({ commit }, query: string) {
      commit('SET_SEARCH_QUERY', query);
    },
  },
};

export default appletsModule;
