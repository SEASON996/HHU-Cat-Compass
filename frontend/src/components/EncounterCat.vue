<template>
  <van-popup
    :show="localVisible"
    position="bottom"
    round
    :style="{ height: '75%' }"
    closeable
    @update:show="handleVisibleChange"
    @closed="handleClosed"
  >
    <div class="encounter-popup">
      <div class="popup-title">偶遇打卡</div>

      <!-- 猫咪选择 -->
      <div class="select-cat-section">
        <div class="section-label">选择猫咪 <span class="required">*</span></div>
        <div class="cat-selector" @click="showCatPicker = true">
          <span v-if="selectedCat">{{ selectedCat.name }} ({{ selectedCat.id }})</span>
          <span v-else class="placeholder">点击选择猫咪</span>
          <van-icon name="arrow" />
        </div>
      </div>

      <!-- 图片上传 / 拍摄 -->
      <div class="upload-section">
        <div class="section-label">上传照片 <span class="required">*</span></div>
        <van-uploader
          v-model="fileList"
          :max-count="1"
          :after-read="afterRead"
          accept="image/*"
          capture="camera"
          :before-read="beforeRead"
        />
        <div class="upload-tip">可拍照或从相册选择（最多1张）</div>
        <div v-if="uploading" class="uploading-tip"><van-loading size="16px" /> 图片上传中...</div>
      </div>

      <!-- 当前位置 -->
      <div class="location-section">
        <div class="section-label">当前位置</div>
        <div class="location-info" v-if="currentLocation">
          <van-icon name="location-o" />
          <span class="location-address">{{ currentLocation.address }}</span>
          <van-button size="small" plain @click="refreshLocation">重新定位</van-button>
        </div>
        <div v-else class="location-info loading-location">
          <van-loading size="16px" /> {{ locationStatus }}
        </div>
      </div>

      <!-- 备注 -->
      <div class="remark-section">
        <div class="section-label">备注（可选）</div>
        <van-field
          v-model="remark"
          type="textarea"
          placeholder="可以补充说明猫咪的状态、位置等信息"
          rows="2"
          autosize
        />
      </div>

      <!-- 提交按钮 -->
      <div class="submit-btn-wrapper">
        <van-button
          type="primary"
          round
          block
          @click="handleSubmit"
          :loading="submitting"
          :disabled="uploading || locationLoading"
        >
          确认并提交
        </van-button>
      </div>
    </div>

    <!-- 猫咪选择器 -->
    <van-action-sheet v-model:show="showCatPicker" title="选择猫咪">
      <div class="cat-picker-list">
        <div v-for="cat in cats" :key="cat.id" class="cat-picker-item" @click="selectCat(cat)">
          <div class="cat-name">{{ cat.name }}</div>
          <div class="cat-info">{{ cat.location_desc }} · {{ cat.campus }}</div>
        </div>
        <div v-if="cats.length === 0" class="empty-tip">暂无猫咪数据</div>
      </div>
    </van-action-sheet>
  </van-popup>
</template>

<script setup>
import { ref, watch } from 'vue'
import { showToast, closeToast } from 'vant'
import { createRecord, uploadImage } from '@/api'

// Props
const props = defineProps({
  visible: { type: Boolean, default: false },
  cats: { type: Array, default: () => [] },
  userId: { type: Number, default: 1 },
})

// Emits
const emit = defineEmits(['update:visible', 'success'])

// 本地状态
const localVisible = ref(props.visible)
const selectedCat = ref(null)
const fileList = ref([])
const currentLocation = ref(null)
const locationLoading = ref(false)
const locationStatus = ref('获取位置中...')
const submitting = ref(false)
const uploading = ref(false)
const showCatPicker = ref(false)
const remark = ref('')
const uploadedImageUrl = ref('')

// 监听 props.visible
watch(
  () => props.visible,
  (val) => {
    localVisible.value = val
    if (val) {
      getCurrentLocation()
    }
  },
)

// 处理弹窗显示/隐藏
const handleVisibleChange = (val) => {
  localVisible.value = val
  emit('update:visible', val)
}

// 获取当前位置
const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    currentLocation.value = { address: '浏览器不支持定位' }
    return
  }

  locationLoading.value = true
  locationStatus.value = '定位中...'

  // 设置超时定时器
  const timeoutId = setTimeout(() => {
    if (locationLoading.value) {
      locationLoading.value = false
      locationStatus.value = '定位超时'
      currentLocation.value = { address: '定位超时，请手动输入位置' }
      showToast('定位超时，请检查GPS')
    }
  }, 10000)

  navigator.geolocation.getCurrentPosition(
    (position) => {
      clearTimeout(timeoutId)
      locationLoading.value = false
      const { latitude, longitude } = position.coords
      currentLocation.value = {
        lat: latitude,
        lng: longitude,
        address: `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`,
      }
      showToast('定位成功')
    },
    (error) => {
      clearTimeout(timeoutId)
      locationLoading.value = false
      console.error('定位失败:', error)

      let errorMsg = '定位失败'
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMsg = '请允许位置权限'
          break
        case error.POSITION_UNAVAILABLE:
          errorMsg = '无法获取位置信息'
          break
        case error.TIMEOUT:
          errorMsg = '定位超时'
          break
      }

      locationStatus.value = errorMsg
      currentLocation.value = { address: errorMsg }
      showToast(errorMsg)
    },
    {
      enableHighAccuracy: false, // 设为 false 加快定位速度
      timeout: 8000,
      maximumAge: 30000, // 30秒内可复用缓存
    },
  )
}

const refreshLocation = () => {
  getCurrentLocation()
}

// 图片上传前验证
const beforeRead = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    showToast('请选择图片文件')
    return false
  }

  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    showToast('图片大小不能超过 5MB')
    return false
  }

  return true
}

// 图片读取完成后上传
const afterRead = async (file) => {
  if (!file.file) return

  uploading.value = true

  // 显示加载提示
  showToast({
    type: 'loading',
    message: '上传中...',
    duration: 0,
  })

  try {
    const res = await uploadImage(file.file)
    uploadedImageUrl.value = res.url || res.data?.url
    closeToast() // 关闭加载提示
    showToast('图片上传成功')
  } catch (error) {
    closeToast()
    console.error('图片上传失败:', error)
    showToast(error.message || '图片上传失败，请重试')
    // 上传失败，清空该图片
    fileList.value = []
    uploadedImageUrl.value = ''
  } finally {
    uploading.value = false
  }
}

const selectCat = (cat) => {
  selectedCat.value = cat
  showCatPicker.value = false
}

const handleSubmit = async () => {
  // 验证
  if (!selectedCat.value) {
    showToast('请选择猫咪')
    return
  }
  if (fileList.value.length === 0 && !uploadedImageUrl.value) {
    showToast('请拍摄或选择一张照片')
    return
  }
  if (!currentLocation.value?.lat) {
    showToast('无法获取有效位置，请检查定位或手动刷新')
    return
  }

  // 如果还在上传中，等待
  if (uploading.value) {
    showToast('请稍后，图片上传中...')
    return
  }

  submitting.value = true

  try {
    // 构建打卡数据
    const recordData = {
      cat_id: selectedCat.value.id,
      user_id: props.userId,
      event_type: '偶遇打卡',
      image_url: uploadedImageUrl.value,
      food_type: null,
      remark: remark.value || null,
      latitude: currentLocation.value.lat,
      longitude: currentLocation.value.lng,
    }

    await createRecord(recordData)

    showToast('打卡成功！')

    // 重置表单
    selectedCat.value = null
    fileList.value = []
    uploadedImageUrl.value = ''
    remark.value = ''
    currentLocation.value = null

    // 关闭弹窗
    handleVisibleChange(false)

    // 通知父组件刷新
    emit('success')
  } catch (error) {
    console.error('打卡失败:', error)
    showToast(error.message || '打卡失败，请重试')
  } finally {
    submitting.value = false
  }
}

const handleClosed = () => {
  if (!localVisible.value) {
    selectedCat.value = null
    fileList.value = []
    uploadedImageUrl.value = ''
    remark.value = ''
  }
}
</script>

<style scoped lang="scss">
.encounter-popup {
  padding: 20px 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
}

.popup-title {
  font-size: 18px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 8px;
}

.section-label {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #323233;

  .required {
    color: #ee0a24;
  }
}

.cat-selector {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;

  .placeholder {
    color: #969799;
  }
}

.upload-tip {
  font-size: 12px;
  color: #969799;
  margin-top: 6px;
}

.uploading-tip {
  font-size: 12px;
  color: #07c160;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f9fa;
  padding: 10px 12px;
  border-radius: 12px;
  font-size: 13px;
}

.location-address {
  flex: 1;
  word-break: break-all;
}

.loading-location {
  color: #969799;
  gap: 6px;
}

.remark-section {
  :deep(.van-field__control) {
    background: #f8f9fa;
    border-radius: 12px;
  }
}

.submit-btn-wrapper {
  margin-top: auto;
  padding: 12px 0;
}

.cat-picker-list {
  max-height: 60vh;
  overflow-y: auto;
}

.cat-picker-item {
  padding: 14px 20px;
  border-bottom: 1px solid #ebedf0;
  cursor: pointer;

  &:active {
    background: #f5f5f5;
  }

  .cat-name {
    font-weight: 500;
    margin-bottom: 4px;
  }

  .cat-info {
    font-size: 12px;
    color: #969799;
  }
}

.empty-tip {
  text-align: center;
  padding: 40px;
  color: #969799;
}
</style>
