import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: async () => ({ top: 0 }),
  routes: [
    {
      path: '/',
      component: async () => import('../pages/HomePage.vue'),
      name: 'home'
    },
    {
      path: '/session',
      component: async () => import('../pages/NewSessionPage.vue'),
      name: 'session'
    },
    {
      path: '/scoring',
      component: async () => import('../pages/ScoringPage.vue'),
      name: 'scoring'
    }
  ]
})

export default router
