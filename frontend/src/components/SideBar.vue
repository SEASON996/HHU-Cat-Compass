<template>
  <div class="sidebar-container">
    <!-- 顶部用户区域（可选的简洁版） -->
    <div class="sidebar-header">
      <div class="logo">
        <span class="logo-icon">🐱</span>
        <span class="logo-text">河海猫咪地图</span>
      </div>
      <van-icon name="cross" class="close-icon" @click="$emit('close')" />
    </div>

    <!-- 导航菜单 -->
    <div class="nav-menu">
      <div
        v-for="item in menuItems"
        :key="item.path"
        class="nav-item"
        :class="{ active: currentPath === item.path }"
        @click="handleNav(item)"
      >
        <van-icon :name="item.icon" class="nav-icon" />
        <span class="nav-label">{{ item.label }}</span>
        <van-icon v-if="item.badge" name="warning-o" class="badge" />
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="sidebar-footer">
      <div class="version">v1.0.0</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const emit = defineEmits(['close', 'navigate'])
const route = useRoute()

const currentPath = computed(() => route.path)

const menuItems = [
  { path: '/map', label: '寻猫地图', icon: 'map-o' },
  { path: '/archive', label: '档案库', icon: 'apps-o' },
]

const handleNav = (item) => {
  emit('navigate', item.path)
}
</script>

<style scoped lang="scss">
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(180deg, #fff 0%, #f8f9fa 100%);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 16px;
  border-bottom: 1px solid #ebedf0;

  .logo {
    display: flex;
    align-items: center;
    gap: 8px;

    .logo-icon {
      font-size: 28px;
    }

    .logo-text {
      font-size: 18px;
      font-weight: 600;
      color: #07c160;
    }
  }

  .close-icon {
    font-size: 20px;
    color: #969799;
    cursor: pointer;
    padding: 4px;
  }
}

.nav-menu {
  flex: 1;
  padding: 20px 0;

  .nav-item {
    display: flex;
    align-items: center;
    padding: 14px 20px;
    margin: 4px 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;

    &.active {
      background: #07c160;
      color: white;

      .nav-icon {
        color: white;
      }
    }

    &:active {
      transform: scale(0.98);
      background: #f0f0f0;
    }

    .nav-icon {
      font-size: 20px;
      margin-right: 12px;
      color: #666;
    }

    .nav-label {
      flex: 1;
      font-size: 15px;
      font-weight: 500;
    }

    .badge {
      color: #ee0a24;
      font-size: 14px;
    }
  }
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #ebedf0;
  text-align: center;

  .version {
    font-size: 12px;
    color: #969799;
  }
}
</style>
