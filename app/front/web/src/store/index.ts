import { createStore } from 'vuex';
import appletsModule, { AppletsState } from './applets';

export interface AppState {
  applets: AppletsState;
}

export default createStore<AppState>({
  modules: {
    applets: appletsModule,
  },
});
