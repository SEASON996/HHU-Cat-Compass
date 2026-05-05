import axios from 'axios'
import { showToast } from 'vant'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)
let message = '请求失败'
// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const status = error.response.status
      const data = error.response.data

      if (data?.detail) {
        message = data.detail
      } else if (status === 400) {
        message = '请求参数错误'
      } else if (status === 404) {
        message = '资源不存在'
      } else if (status === 500) {
        message = '服务器错误'
      } else {
        message = `请求失败 (${status})`
      }
    } else if (error.request) {
      message = '网络连接失败，请检查网络'
    } else {
      message = error.message || '请求失败'
    }

    showToast(message)
    return Promise.reject(new Error(message))
  },
)

export default request
