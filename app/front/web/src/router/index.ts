import { createRouter, createWebHistory } from 'vue-router';
import SignInView from '../views/auth/SignInView.vue';
import SignUpView from '../views/auth/SignUpView.vue';
import ForgotPasswordView from '../views/auth/forgotpwd/ForgotPasswordView.vue';
import ResetPasswordView from '../views/auth/forgotpwd/ResetPasswordView.vue';

const routes = [
  { path: '/', name: '', component: SignInView },
  { path: '/sign-in', name: 'SignIn', component: SignInView },
  { path: '/sign-up', name: 'SignUp', component: SignUpView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },
  { path: '/forgot-password/reset-password', name: 'ResetPassword', component: ResetPasswordView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
