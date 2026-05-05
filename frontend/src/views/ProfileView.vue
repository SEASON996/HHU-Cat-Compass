<template>
  <div class="profile-page">
    <!-- 已登录状态 -->
    <div v-if="userStore.isLoggedIn" class="profile-content">
      <div class="profile-header">
        <div class="avatar">
          <van-icon name="user-circle-o" size="60" color="#07c160" />
        </div>
        <div class="username">{{ userStore.userName }}</div>
        <div class="student-id">{{ userStore.studentId }}</div>
        <div class="role-badge" :class="userStore.isAdmin ? 'admin' : 'user'">
          {{ userStore.isAdmin ? '管理员' : '普通用户' }}
        </div>
        <div class="logout-tip">
          <van-button type="danger" size="small" plain @click="handleLogout">退出登录</van-button>
        </div>
      </div>

      <div class="menu-list">
        <div class="menu-item" @click="goToMyRecords">
          <van-icon name="records-o" />
          <span>我的打卡</span>
          <van-icon name="arrow" />
        </div>
        <div class="menu-item" @click="showAbout">
          <van-icon name="info-o" />
          <span>关于我们</span>
          <van-icon name="arrow" />
        </div>
      </div>
    </div>

    <!-- 未登录状态 -->
    <div v-else class="not-logged-in">
      <div class="login-prompt">
        <van-icon name="user-circle-o" size="80" color="#c8c9cc" />
        <p>登录后可以查看个人打卡记录</p>
        <van-button type="primary" round @click="goToLogin">立即登录</van-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { showConfirmDialog, showToast } from 'vant'

const router = useRouter()
const userStore = useUserStore()

const goToLogin = () => {
  router.push('/login')
}

const goToMyRecords = () => {
  router.push('/my-records')
}

const handleLogout = async () => {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定要退出登录吗？',
    })
    userStore.logout()
    showToast('已退出登录')
    // 刷新当前页面，清除状态
    router.go(0)
  } catch {
    // 用户取消
  }
}

const showAbout = () => {
  showToast('河海猫咪地图 v1.0.0')
}
</script>

<style scoped lang="scss">
.profile-page {
  background: #f5f5f5;
  min-height: 100vh;
}

.profile-header {
  background: white;
  padding: 30px 20px;
  text-align: center;
  margin-bottom: 12px;

  .avatar {
    margin-bottom: 12px;
  }

  .username {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
    color: #323233;
  }

  .student-id {
    font-size: 14px;
    color: #969799;
    margin-bottom: 12px;
  }

  .role-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin-bottom: 16px;

    &.user {
      background: #e8f8f0;
      color: #07c160;
    }

    &.admin {
      background: #fff0e8;
      color: #ff976a;
    }
  }

  .logout-tip {
    margin-top: 8px;
  }
}

.menu-list {
  background: white;

  .menu-item {
    display: flex;
    align-items: center;
    padding: 14px 16px;
    border-bottom: 1px solid #ebedf0;
    cursor: pointer;

    &:active {
      background: #f5f5f5;
    }

    .van-icon:first-child {
      font-size: 20px;
      color: #07c160;
      margin-right: 12px;
    }

    span {
      flex: 1;
      font-size: 15px;
    }

    .van-icon:last-child {
      color: #969799;
      font-size: 14px;
    }
  }
}

.not-logged-in {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;

  .login-prompt {
    text-align: center;
    padding: 40px;

    .van-icon {
      margin-bottom: 20px;
    }

    p {
      font-size: 14px;
      color: #969799;
      margin-bottom: 24px;
    }
  }
}
</style>
