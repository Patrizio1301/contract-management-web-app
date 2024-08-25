import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  mode: 'history',
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/contract',
      name: 'contract',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ContractTable.vue')
    },
    {
      path: '/contract-questions',
      name: 'contract-questions',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ContractQA.vue')
    },
    {
      path: '/contract-question-list',
      name: 'contract-question-list',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/QAList.vue')
    }
  ]
})

export default router
