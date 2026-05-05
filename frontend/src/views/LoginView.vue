<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { showToast } from 'vant'

const router = useRouter()
const userStore = useUserStore()

const studentId = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!studentId.value.trim()) {
    showToast('请输入学号')
    return
  }

  loading.value = true
  try {
    await userStore.loginUser(studentId.value.trim())
    showToast('登录成功')
    router.push('/profile')
  } catch (error) {
    showToast(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo">
        <span class="logo-icon">🐱</span>
        <h1>河海猫咪地图</h1>
        <p>记录校园猫咪的点点滴滴</p>
      </div>

      <van-form @submit="handleLogin">
        <van-field
          v-model="studentId"
          name="student_id"
          label="学号"
          placeholder="请输入学号"
          :rules="[{ required: true, message: '请填写学号' }]"
        />
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" :loading="loading">
            登录 / 注册
          </van-button>
        </div>
      </van-form>

      <div class="tip">首次登录将自动注册</div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #07c160 0%, #06ad56 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 24px;
  padding: 32px 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.logo {
  text-align: center;
  margin-bottom: 32px;

  .logo-icon {
    font-size: 48px;
  }

  h1 {
    font-size: 24px;
    color: #323233;
    margin: 12px 0 8px;
  }

  p {
    font-size: 14px;
    color: #969799;
  }
}

.submit-btn {
  margin-top: 24px;
}

.tip {
  text-align: center;
  font-size: 12px;
  color: #969799;
  margin-top: 16px;
}
</style>
