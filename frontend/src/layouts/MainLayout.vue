<template>
  <div class="main-layout">
    <!-- 顶部导航栏 -->
    <div class="top-navbar">
      <div class="navbar-left">
        <van-icon v-if="canGoBack" name="arrow-left" class="back-icon" @click="goBack" />
      </div>
      <div class="navbar-title">{{ currentTitle }}</div>
      <div class="navbar-right">
        <router-link v-if="!userStore.isLoggedIn" to="/login">
          <van-icon name="user-o" />
        </router-link>
        <router-link v-else to="/profile">
          <van-icon name="user-o" />
        </router-link>
      </div>
    </div>

    <!-- 主内容区（自动填充剩余空间） -->
    <div class="main-content">
      <router-view />
    </div>

    <!-- 底部导航栏（不固定，自然在底部） -->
    <van-tabbar v-model="activeTab" @change="onTabChange" fixed>
      <van-tabbar-item name="map" icon="map-o">寻猫地图</van-tabbar-item>
      <van-tabbar-item name="archive" icon="apps-o">档案库</van-tabbar-item>
      <van-tabbar-item name="profile" icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('map')

const currentTitle = computed(() => {
  const titles = {
    '/map': '寻猫地图',
    '/archive': '全校猫咪档案',
  }
  if (route.path.startsWith('/cat/')) return '猫咪详情'
  if (route.path.startsWith('/record')) return '打卡'
  if (route.path === '/profile') return '我的'
  return titles[route.path] || '河海猫咪地图'
})

const canGoBack = computed(() => {
  return route.path !== '/map' && route.path !== '/archive' && route.path !== '/profile'
})

watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/map') {
      activeTab.value = 'map'
    } else if (newPath === '/archive') {
      activeTab.value = 'archive'
    } else if (newPath === '/profile') {
      activeTab.value = 'profile'
    }
  },
  { immediate: true },
)

const onTabChange = (name) => {
  router.push(`/${name}`)
}

const goBack = () => {
  router.back()
}

const handleSearch = () => {
  if (route.path === '/archive') {
    window.dispatchEvent(new CustomEvent('global-search'))
  } else {
    router.push('/archive')
  }
}
</script>

<style scoped lang="scss">
.main-layout {
  height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

// 顶部导航栏（不固定）
.top-navbar {
  flex-shrink: 0; // 不压缩
  height: 46px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid #ebedf0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);

  .navbar-left {
    width: 44px;

    .back-icon {
      font-size: 22px;
      cursor: pointer;
    }
  }

  .navbar-title {
    font-size: 18px;
    font-weight: 600;
    color: #323233;
  }

  .navbar-right {
    width: 44px;
    text-align: right;

    .van-icon {
      font-size: 20px;
      cursor: pointer;
    }
  }
}

// 主内容区
.main-content {
  flex: 1;
  min-height: 0; // 关键：flex 子项需要 min-height:0 才能正确收缩
}
// 底部导航栏
:deep(.van-tabbar) {
  flex-shrink: 0; // 不压缩
  border-top: 1px solid #ebedf0;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.van-tabbar-item--active) {
  color: #07c160;
}
</style>
