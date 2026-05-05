<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCatStore } from '@/stores/cat'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const catStore = useCatStore()

const catId = route.params.id
const cat = ref(null)
const records = ref([])
const stats = ref(null)
const loading = ref(true)
const showPreview = ref(false)
const previewUrl = ref('')

// 状态样式
const statusClass = ref('')
const healthClass = ref('')

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    cat.value = await catStore.fetchCatById(catId)
    records.value = await catStore.fetchCatRecords(catId, { limit: 20 })
    stats.value = await catStore.fetchCatStats(catId)

    // 设置样式类
    const statusMap = {
      正常: 'status-normal',
      需救助: 'status-help',
      已绝育: 'status-neutered',
      已领养: 'status-adopted',
      失踪: 'status-missing',
    }
    statusClass.value = statusMap[cat.value?.current_status] || ''

    const healthMap = { 正常: 'health-normal', 需救助: 'health-help', 已绝育: 'health-neutered' }
    healthClass.value = healthMap[cat.value?.health_status] || ''
  } catch (error) {
    showToast(error)
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const hours = diff / (1000 * 60 * 60)

  if (hours < 1) return '刚刚'
  if (hours < 24) return `${Math.floor(hours)}小时前`
  if (hours < 48) return '昨天'
  return `${Math.floor(hours / 24)}天前`
}

// 预览图片
const previewImage = (url) => {
  previewUrl.value = url
  showPreview.value = true
}

// 去打卡
const goToRecord = () => {
  router.push(`/record/${catId}`)
}

// 图片加载失败时，替换成本地 SVG
const handleImageError = (e) => {
  // 防止无限循环：如果已经是默认 SVG，则不再处理
  if (e.target.src?.startsWith('data:image/svg+xml')) return

  // 自定义一个可爱的猫咪占位图 SVG
  const svgPlaceholder = `
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <rect width="200" height="200" fill="#f0f0f0"/>
    <text x="100" y="120" text-anchor="middle" font-size="64" fill="#bbb">🐱</text>
    <text x="100" y="170" text-anchor="middle" font-size="24" fill="#aaa">暂无照片</text>
  </svg>
  `
  e.target.src = `data:image/svg+xml,${encodeURIComponent(svgPlaceholder)}`
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="cat-detail" v-if="cat">
    <!-- 猫咪照片 -->
    <div class="cat-image">
      <img :src="cat.photo_url" @error="handleImageError" />
    </div>

    <!-- 基本信息 -->
    <div class="info-card">
      <div class="cat-header">
        <h1>{{ cat.name }}</h1>
        <span class="status" :class="statusClass">{{ cat.current_status }}</span>
      </div>

      <div class="info-list">
        <div class="info-row">
          <span class="label">性别</span>
          <span>{{ cat.gender }}</span>
        </div>
        <div class="info-row">
          <span class="label">年龄</span>
          <span>{{ cat.age_stage }}</span>
        </div>
        <div class="info-row">
          <span class="label">毛色</span>
          <span>{{ cat.coat_color }}</span>
        </div>
        <div class="info-row">
          <span class="label">健康状况</span>
          <span :class="healthClass">{{ cat.health_status }}</span>
        </div>
        <div class="info-row">
          <span class="label">校区</span>
          <span>{{ cat.campus }}</span>
        </div>
        <div class="info-row">
          <span class="label">常出没</span>
          <span>{{ cat.location_desc }}</span>
        </div>
        <div class="info-row" v-if="cat.remark">
          <span class="label">备注</span>
          <span>{{ cat.remark }}</span>
        </div>
      </div>

      <!-- 统计 -->
      <div class="stats">
        <div class="stat">
          <div class="num">{{ stats?.total_records || 0 }}</div>
          <div class="label">总打卡</div>
        </div>
        <div class="stat">
          <div class="num">{{ stats?.sighting_count || 0 }}</div>
          <div class="label">偶遇</div>
        </div>
        <div class="stat">
          <div class="num">{{ stats?.feeding_count || 0 }}</div>
          <div class="label">投喂</div>
        </div>
      </div>

      <!-- 打卡按钮 -->
      <van-button type="primary" round block @click="goToRecord"> 📍 打卡 </van-button>
    </div>

    <!-- 打卡记录 -->
    <div class="records-card">
      <div class="title">最新打卡记录</div>
      <div v-if="records.length === 0" class="empty">暂无打卡记录</div>
      <div v-else class="record-list">
        <div v-for="record in records" :key="record.id" class="record-item">
          <div
            class="record-type"
            :class="record.event_type === '偶遇打卡' ? 'sighting' : 'feeding'"
          >
            {{ record.event_type === '偶遇打卡' ? '👀' : '🍖' }}
          </div>
          <div class="record-info">
            <div class="type">{{ record.event_type }}</div>
            <div class="time">{{ formatDate(record.created_at) }}</div>
            <div v-if="record.food_type" class="food">食物：{{ record.food_type }}</div>
          </div>
          <img
            v-if="record.image_url"
            :src="record.image_url"
            class="record-img"
            @click="previewImage(record.image_url)"
          />
        </div>
      </div>
    </div>

    <!-- 图片预览 -->
    <van-image-preview v-model:show="showPreview" :images="[previewUrl]" />
  </div>

  <!-- 加载中 -->
  <div v-else-if="loading" class="loading">
    <van-loading />
  </div>
</template>

<style scoped lang="scss">
.cat-detail {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.cat-image {
  height: 300px;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.info-card {
  background: white;
  margin: 12px;
  padding: 16px;
  border-radius: 16px;
}

.cat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  h1 {
    font-size: 22px;
    margin: 0;
  }

  .status {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    color: white;

    &.status-normal {
      background: #07c160;
    }
    &.status-help {
      background: #ff976a;
    }
    &.status-neutered {
      background: #1989fa;
    }
    &.status-adopted {
      background: #ff9ecf;
    }
    &.status-missing {
      background: #969799;
    }
  }
}

.info-list {
  .info-row {
    display: flex;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;

    .label {
      width: 80px;
      color: #969799;
    }

    .health-normal {
      color: #07c160;
    }
    .health-help {
      color: #ff976a;
    }
    .health-neutered {
      color: #1989fa;
    }
  }
}

.stats {
  display: flex;
  justify-content: space-around;
  padding: 16px 0;
  margin: 16px 0;
  background: #f8f9fa;
  border-radius: 12px;

  .stat {
    text-align: center;

    .num {
      font-size: 24px;
      font-weight: bold;
      color: #323233;
    }

    .label {
      font-size: 12px;
      color: #969799;
    }
  }
}

.records-card {
  background: white;
  margin: 12px;
  padding: 16px;
  border-radius: 16px;

  .title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 16px;
  }

  .empty {
    text-align: center;
    padding: 32px;
    color: #969799;
  }
}

.record-list {
  .record-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;

    .record-type {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;

      &.sighting {
        background: #e8f0fe;
      }
      &.feeding {
        background: #fff0e8;
      }
    }

    .record-info {
      flex: 1;

      .type {
        font-weight: 500;
        margin-bottom: 4px;
      }

      .time {
        font-size: 12px;
        color: #969799;
      }

      .food {
        font-size: 12px;
        color: #07c160;
        margin-top: 2px;
      }
    }

    .record-img {
      width: 50px;
      height: 50px;
      border-radius: 8px;
      object-fit: cover;
    }
  }
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
