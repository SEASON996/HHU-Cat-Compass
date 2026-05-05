import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, getCurrentUser } from '@/api'
import { setToken, getToken, removeToken, setUser, getUser, removeUser } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(getUser())
  const token = ref(getToken())
  const loading = ref(false)
  const error = ref(null)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userId = computed(() => user.value?.id)
  const userName = computed(() => user.value?.username || '未登录')
  const studentId = computed(() => user.value?.student_id || '')

  // 登录（无密码）
  const loginUser = async (student_id) => {
    loading.value = true
    error.value = null

    try {
      const res = await login({ student_id })

      // 保存 token 和用户信息
      setToken(res.access_token)
      setUser({
        id: res.user_id,
        student_id: res.student_id,
        username: res.username,
        role: res.role,
      })

      token.value = res.access_token
      user.value = {
        id: res.user_id,
        student_id: res.student_id,
        username: res.username,
        role: res.role,
      }

      return res
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || '登录失败'
      error.value = errorMessage
      throw new Error(errorMessage, { cause: err }) // 抛出错误让调用方捕获
    } finally {
      loading.value = false
    }
  }

  // 获取当前用户信息（从 token 恢复）
  const fetchCurrentUser = async () => {
    if (!token.value) return

    try {
      const res = await getCurrentUser()
      if (res) {
        user.value = {
          id: res.id,
          student_id: res.student_id,
          username: res.username,
          role: res.role,
        }
        setUser(user.value)
      }
    } catch (err) {
      console.error('获取用户信息失败:', err)
      // token 可能已过期
      logout()
    }
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = null
    removeToken()
    removeUser()
  }

  // 初始化：从本地存储恢复
  const init = () => {
    const savedToken = getToken()
    const savedUser = getUser()
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = savedUser
      // 可选：验证 token 是否有效
      fetchCurrentUser()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    isAdmin,
    userId,
    userName,
    studentId,
    loginUser,
    fetchCurrentUser,
    logout,
    init,
  }
})
