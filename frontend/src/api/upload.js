import request from '@/utils/request'

// 上传图片
export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)

  return request.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
