import request from '@/utils/request'

// ========== 猫咪接口 ==========
export const getCats = (params) => request.get('/cats', { params })
export const getCatById = (id) => request.get(`/cats/${id}`)
export const getCatRecords = (catId, params) => request.get(`/records/cat/${catId}`, { params })
export const getCatStats = (catId) => request.get(`/records/stats/cat/${catId}`)

// ========== 打卡记录接口 ==========
export const createRecord = (data) => request.post('/records', data)

// ========== 图片上传接口 ==========
export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)

  return request.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

// 认证接口
export const login = (data) => request.post('/auth/login', data)
export const getCurrentUser = () => request.get('/auth/me')
