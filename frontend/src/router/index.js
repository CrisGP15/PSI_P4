import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '../stores/auth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/log-in',
      name: 'login',
      component: () => import('../views/Login.vue'),
      // Si ya está logueado, redirigir a home
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (authStore.isLoggedIn) {
          next({ name: 'home' })
        } else {
          next()
        }
    },
    },
     {
      path: '/log-out',
      name: 'logout',
      component: () => import('../views/Logout.vue')
    },
    {
      path: '/songs/:id',  
      name: 'songs',
      component: () => import('../views/PlayView.vue'),
      props: true
    },
    {
      path: '/faq',  
      name: 'faq',
      component: () => import('../views/FaqView.vue')
    },
    {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
   
  ]

})

export default router
