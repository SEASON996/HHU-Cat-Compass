import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/map',
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import('@/views/MapView.vue'),
    meta: { title: '寻猫地图', requiresAuth: false },
  },
  {
    path: '/archive',
    name: 'Archive',
    component: () => import('@/views/ArchiveView.vue'),
    meta: { title: '档案库', requiresAuth: false },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { title: '我的', requiresAuth: true }, // 需要登录
  },
  {
    path: '/cat/:id',
    name: 'CatDetail',
    component: () => import('@/views/CatDetail.vue'),
    meta: { title: '猫咪详情', requiresAuth: false },
  },
  {
    path: '/record/:catId?',
    name: 'Record',
    component: () => import('@/views/RecordView.vue'),
    meta: { title: '打卡', requiresAuth: true }, // 需要登录
  },
  // {
  //   path: '/my-records',
  //   name: 'MyRecords',
  //   component: () => import('@/views/MyRecords.vue'),
  //   meta: { title: '我的打卡', requiresAuth: true },
  // },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录', requiresAuth: false, hideNav: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 修复：不使用 next 回调，直接返回
router.beforeEach((to, from) => {
  const userStore = useUserStore()

  // 初始化用户状态（从 localStorage 恢复）
  if (!userStore.user && !userStore.token) {
    userStore.init()
  }

  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    }
  }

  // 允许访问
  return true
})

export default router
