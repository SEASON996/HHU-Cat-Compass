<template>
  <div class="record-page">
    <van-form @submit="onSubmit">
      <!-- 猫咪选择 -->
      <van-field
        name="cat"
        label="选择猫咪"
        :value="selectedCat?.name"
        placeholder="点击选择猫咪"
        readonly
        is-link
        @click="showCatPicker = true"
        :rules="[{ required: true, message: '请选择猫咪' }]"
      />

      <!-- 打卡类型 -->
      <van-field name="event_type" label="打卡类型" required>
        <template #input>
          <van-radio-group v-model="form.event_type" direction="horizontal">
            <van-radio name="偶遇打卡">偶遇</van-radio>
            <van-radio name="投喂打卡">投喂</van-radio>
          </van-radio-group>
        </template>
      </van-field>

      <!-- 食物类型（投喂时显示） -->
      <van-field
        v-if="form.event_type === '投喂打卡'"
        v-model="form.food_type"
        label="食物"
        placeholder="请输入食物类型（如：猫粮、罐头）"
      />

      <!-- 图片上传 -->
      <van-field label="打卡照片">
        <template #input>
          <van-uploader v-model="fileList" :max-count="1" />
        </template>
      </van-field>

      <!-- 当前位置 -->
      <div class="location-section">
        <div class="location-header">
          <span>当前位置</span>
          <van-button size="small" type="primary" plain @click="getLocation"> 重新定位 </van-button>
        </div>
        <div class="location-info" v-if="location">
          <van-icon name="location-o" />
          <span>{{ location.address || `${location.latitude}, ${location.longitude}` }}</span>
        </div>
        <div v-else class="location-tip">
          <van-icon name="guide-o" />
          <span>点击获取当前位置</span>
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="submit-btn">
        <van-button round block type="primary" native-type="submit" :loading="submitting">
          提交打卡
        </van-button>
      </div>
    </van-form>

    <!-- 猫咪选择弹窗 -->
    <van-action-sheet v-model:show="showCatPicker" title="选择猫咪">
      <div class="cat-picker">
        <van-search v-model="searchText" placeholder="搜索猫咪" />
        <div class="cat-list">
          <div v-for="cat in filteredCats" :key="cat.id" class="cat-option" @click="selectCat(cat)">
            <img :src="cat.photo_url" />
            <div class="cat-info">
              <div class="name">{{ cat.name }}</div>
              <div class="desc">{{ cat.campus }} · {{ cat.location_desc }}</div>
            </div>
          </div>
          <EmptyState v-if="filteredCats.length === 0" text="暂无猫咪" />
        </div>
      </div>
    </van-action-sheet>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCatStore } from '@/stores/cat'
import { createRecord } from '@/api'
import { showToast } from 'vant'
import EmptyState from '@/components/EmptyState.vue'

const router = useRouter()
const route = useRoute()
const catStore = useCatStore()

const submitting = ref(false)
const showCatPicker = ref(false)
const selectedCat = ref(null)
const searchText = ref('')
const location = ref(null)
const fileList = ref([])

const form = ref({
  cat_id: '',
  event_type: '偶遇打卡',
  food_type: '',
  image_url: '',
})

// 猫咪列表
const cats = ref([])
const filteredCats = computed(() => {
  if (!searchText.value) return cats.value
  return cats.value.filter((cat) => cat.name.includes(searchText.value))
})

// 加载猫咪列表
const loadCats = async () => {
  await catStore.fetchCats()
  cats.value = catStore.cats
}

// 选择猫咪
const selectCat = (cat) => {
  selectedCat.value = cat
  form.value.cat_id = cat.id
  showCatPicker.value = false
}

// 获取位置
const getLocation = () => {
  if (navigator.geolocation) {
    showToast({ type: 'loading', message: '定位中...', duration: 0 })
    navigator.geolocation.getCurrentPosition(
      (position) => {
        showToast.clear()
        location.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          address: `${position.coords.latitude.toFixed(6)}, ${position.coords.longitude.toFixed(6)}`,
        }
        showToast('定位成功')
      },
      (error) => {
        showToast.clear()
        showToast('定位失败，请手动输入位置')
        console.error('定位失败:', error)
      },
    )
  } else {
    showToast('浏览器不支持定位')
  }
}

// 上传图片（简化版）
const uploadImage = async () => {
  if (fileList.value.length === 0) return ''
  // TODO: 实现真实的图片上传
  return fileList.value[0].url || ''
}

// 提交打卡
const onSubmit = async () => {
  if (!form.value.cat_id) {
    showToast('请选择猫咪')
    return
  }

  if (!form.value.event_type) {
    showToast('请选择打卡类型')
    return
  }

  submitting.value = true

  try {
    const imageUrl = await uploadImage()

    const recordData = {
      cat_id: form.value.cat_id,
      event_type: form.value.event_type,
      food_type: form.value.event_type === '投喂打卡' ? form.value.food_type : null,
      image_url: imageUrl || null,
      user_id: 1, // 临时用户ID，后续替换为真实用户
    }

    await createRecord(recordData)
    showToast('打卡成功！')

    // 跳转回猫咪详情页
    if (form.value.cat_id) {
      router.push(`/cat/${form.value.cat_id}`)
    } else {
      router.push('/archive')
    }
  } catch (error) {
    showToast(error.message || '打卡失败')
  } finally {
    submitting.value = false
  }
}

// 如果路由参数有猫咪ID，自动选中
onMounted(async () => {
  await loadCats()

  const catId = route.params.catId
  if (catId) {
    const cat = cats.value.find((c) => c.id === catId)
    if (cat) {
      selectCat(cat)
    }
  }
})
</script>

<style scoped lang="scss">
.record-page {
  padding: 16px;
  padding-bottom: 40px;
}

.location-section {
  background: #f8f9fa;
  border-radius: 12px;
  margin: 16px 0;
  padding: 12px;

  .location-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;
    color: #666;
  }

  .location-info,
  .location-tip {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #969799;
  }

  .location-tip {
    color: #07c160;
  }
}

.submit-btn {
  margin-top: 32px;
}

.cat-picker {
  height: 60vh;
  overflow-y: auto;

  .cat-option {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-bottom: 1px solid #ebedf0;
    cursor: pointer;

    &:active {
      background: #f5f5f5;
    }

    img {
      width: 50px;
      height: 50px;
      border-radius: 8px;
      object-fit: cover;
    }

    .cat-info {
      flex: 1;

      .name {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 4px;
      }

      .desc {
        font-size: 12px;
        color: #969799;
      }
    }
  }
}
</style>
