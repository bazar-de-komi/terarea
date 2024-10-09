import { createRouter, createWebHistory } from 'vue-router';
import SignInView from '../views/auth/SignInView.vue';
import SignUpView from '../views/auth/SignUpView.vue';
import ForgotPasswordView from '../views/auth/forgotpwd/ForgotPasswordView.vue';
import ResetPasswordView from '../views/auth/forgotpwd/ResetPasswordView.vue';
import AreaPageAll from '../views/board/AreaPage-All.vue';
import AreaPageApplet from '../views/board/AreaPage-Applet.vue';
import AreaPageService from '../views/board/AreaPage-Service.vue';
import AppletDetails from '../views/AppletDetails.vue';

const routes = [
  { path: '/', name: '', component: SignInView },
  { path: '/sign-in', name: 'SignIn', component: SignInView },
  { path: '/sign-up', name: 'SignUp', component: SignUpView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },
  { path: '/forgot-password/reset-password', name: 'ResetPassword', component: ResetPasswordView },
  { path: '/explore/all', name: 'AreaExploreAll', component: AreaPageAll },
  { path: '/explore/applets', name: 'AreaExploreApplet', component: AreaPageApplet },
  { path: '/explore/services', name: 'AreaExploreService', component: AreaPageService },
  { path: '/applet/:title', name: 'AppletDetails', component: AppletDetails },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
