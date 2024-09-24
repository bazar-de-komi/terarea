import { createRouter, createWebHistory } from 'vue-router';
import SignInView from '../views/auth/SignInView.vue';
import SignUpView from '../views/auth/SignUpView.vue';
import ForgotPasswordView from '../views/auth/ForgotPasswordView.vue';

const routes = [
  { path: '/', name: '', component: SignInView },
  { path: '/sign-in', name: 'SignIn', component: SignInView },
  { path: '/sign-up', name: 'SignUp', component: SignUpView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
