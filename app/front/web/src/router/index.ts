import { createRouter, createWebHistory } from 'vue-router';
import SignInView from '../views/auth/SignInView.vue';
import SignUpView from '../views/auth/SignUpView.vue';
import ForgotPasswordView from '../views/auth/forgotpwd/ForgotPasswordView.vue';
import ResetPasswordView from '../views/auth/forgotpwd/ResetPasswordView.vue';
import AreaPageAll from '../views/board/AreaPage-All.vue';
import AppletDetails from '../views/tile-information/AppletDetails.vue';
import ServiceDetails from '../views/tile-information/ServiceDetails.vue';
import CreateApplet from '@/views/create/CreateApplet.vue';
import DisplayAction from '@/views/create/DisplayAction.vue';
import DisplayTrigger from '@/views/create/DisplayTrigger.vue';
import MainPage from '@/views/main/MainPage.vue';
import ProfilePage from '@/views/profil/AccountSetting.vue';
import ChangePassword from '@/views/profil/ChangePassword.vue'
import CallbackView from '@/views/auth/CallbackView.vue';
import TriggerInformation from '@/views/create/TriggerInformation.vue';
import ReactionInformation from '@/views/create/ActionInformation.vue';

const routes = [
  { path: '/', name: 'MainPage', component: MainPage },
  { path: '/sign-in', name: 'SignIn', component: SignInView },
  { path: '/sign-up', name: 'SignUp', component: SignUpView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },
  { path: '/forgot-password/reset-password', name: 'ResetPassword', component: ResetPasswordView },
  { path: '/callback', name: 'CallbackView', component: CallbackView },
  { path: '/explore/applets', name: 'AreaExploreAll', component: AreaPageAll },
  { path: '/applet/:title', name: 'AppletDetails', component: AppletDetails },
  { path: '/service/:title', name: 'ServiceDetails', component: ServiceDetails },
  { path: '/create', name: 'CreateApplet', component: CreateApplet },
  { path: '/create/add-action', name: 'DisplayAction', component: DisplayAction },
  { path: '/create/add-trigger', name: 'DisplayTrigger', component: DisplayTrigger },
  { path: '/create/add-trigger/trigger-detail', name: 'TriggerInformation', component: TriggerInformation},
  { path: '/create/add-action/reaction-detail', name: 'ReactionInformation', component: ReactionInformation},
  { path: '/account', name: 'ProfilePage', component: ProfilePage },
  { path: '/account/change-password', name: 'ChangePassword', component: ChangePassword },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
