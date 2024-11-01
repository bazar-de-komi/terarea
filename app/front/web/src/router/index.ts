import { createRouter, createWebHistory } from 'vue-router';
import SignInView from '../views/auth/SignInView.vue';
import SignUpView from '../views/auth/SignUpView.vue';
import ForgotPasswordView from '../views/auth/forgotpwd/ForgotPasswordView.vue';
import ResetPasswordView from '../views/auth/forgotpwd/ResetPasswordView.vue';
import AreaPageAll from '../views/board/AreaPage-All.vue';
import AreaPageApplet from '../views/board/AreaPage-Applet.vue';
import AreaPageService from '../views/board/AreaPage-Service.vue';
import AppletDetails from '../views/tile-information/AppletDetails.vue';
import ServiceDetails from '../views/tile-information/ServiceDetails.vue';
import CreateApplet from '@/views/CreateApplet.vue';
import DisplayAction from '@/views/temp/DisplayAction.vue';
import DisplayReaction from '@/views/temp/DisplayReaction.vue';
import MainPage from '@/views/main/MainPage.vue';
import ProfilePage from '@/views/profil/AccountSetting.vue';
import ChangePassword from '@/views/profil/ChangePassword.vue'

const routes = [
  { path: '/', name: 'MainPage', component: MainPage },
  { path: '/sign-in', name: 'SignIn', component: SignInView },
  { path: '/sign-up', name: 'SignUp', component: SignUpView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },
  { path: '/forgot-password/reset-password', name: 'ResetPassword', component: ResetPasswordView },
  { path: '/explore/all', name: 'AreaExploreAll', component: AreaPageAll },
  { path: '/explore/applets', name: 'AreaExploreApplet', component: AreaPageApplet },
  { path: '/explore/services', name: 'AreaExploreService', component: AreaPageService },
  { path: '/applet/:title', name: 'AppletDetails', component: AppletDetails },
  { path: '/service/:title', name: 'ServiceDetails', component: ServiceDetails },
  { path: '/create', name: 'CreateApplet', component: CreateApplet },
  { path: '/create/add-action', name: 'DisplayAction', component: DisplayAction },
  { path: '/create/add-reaction', name: 'DisplayReaction', component: DisplayReaction },
  { path: '/account', name: 'ProfilePage', component: ProfilePage },
  { path: '/account/change-password', name: 'ChangePassword', component: ChangePassword },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
