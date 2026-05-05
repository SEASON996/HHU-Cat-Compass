<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCatStore } from '@/stores/cat'
import CatCard from '@/components/CatCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import { showToast } from 'vant'

const router = useRouter()
const catStore = useCatStore()

// 搜索和筛选
const searchKeyword = ref('')
const selectedCampus = ref('')
const selectedStatus = ref('')
const selectedGender = ref('')

// 选择器显示状态
const showCampusPicker = ref(false)
const showStatusPicker = ref(false)
const showGenderPicker = ref(false)

// 列表状态
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const error = ref(false)
const currentPage = ref(1)
const pageSize = 10
const catList = ref([])

// 统计数据
const totalCount = ref(0)
const needHelpCount = ref(0)
const normalCount = ref(0)

// 选项配置
const campusOptions = [
  { label: '全部校区', value: '' },
  { label: '江宁', value: '江宁' },
  { label: '西康路', value: '西康路' },
  { label: '金坛', value: '金坛' },
]

const statusOptions = [
  { label: '全部状态', value: '' },
  { label: '正常', value: '正常' },
  { label: '需救助', value: '需救助' },
  { label: '已绝育', value: '已绝育' },
  { label: '已领养', value: '已领养' },
  { label: '失踪', value: '失踪' },
]

const genderOptions = [
  { label: '全部性别', value: '' },
  { label: '公', value: '公' },
  { label: '母', value: '母' },
  { label: '未知', value: '未知' },
]

// 监听全局搜索事件
const handleGlobalSearch = () => {
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
  // 触发搜索
  onSearch()
}

// 快速筛选
const quickFilter = (status) => {
  if (status === 'all') {
    selectedStatus.value = ''
  } else {
    selectedStatus.value = status
  }
  resetAndSearch()
}

// 选择校区
const selectCampus = (campus) => {
  selectedCampus.value = campus
  showCampusPicker.value = false
  resetAndSearch()
}

// 选择状态
const selectStatus = (status) => {
  selectedStatus.value = status
  showStatusPicker.value = false
  resetAndSearch()
}

// 选择性别
const selectGender = (gender) => {
  selectedGender.value = gender
  showGenderPicker.value = false
  resetAndSearch()
}

// 重置并搜索
const resetAndSearch = () => {
  currentPage.value = 1
  catList.value = []
  finished.value = false
  loading.value = true
  loadCats()
}

// 搜索
const onSearch = () => {
  resetAndSearch()
}

// 刷新
const onRefresh = () => {
  refreshing.value = true
  currentPage.value = 1
  catList.value = []
  finished.value = false
  loadCats()
}

// 加载猫咪列表
const loadCats = async () => {
  error.value = false

  const params = {
    skip: (currentPage.value - 1) * pageSize,
    limit: pageSize,
  }

  if (searchKeyword.value) {
    params.name = searchKeyword.value
  }
  if (selectedCampus.value) {
    params.campus = selectedCampus.value
  }
  if (selectedStatus.value) {
    params.status = selectedStatus.value
  }
  if (selectedGender.value) {
    params.gender = selectedGender.value
  }

  try {
    const res = await catStore.fetchCats(params)
    const newCats = Array.isArray(res) ? res : []

    if (refreshing.value) {
      catList.value = newCats
      refreshing.value = false
    } else {
      catList.value = [...catList.value, ...newCats]
    }

    loading.value = false

    if (newCats.length < pageSize) {
      finished.value = true
    }

    currentPage.value++

    // 更新统计数据
    await loadStats()
  } catch (error) {
    error.value = true
    loading.value = false
    if (refreshing.value) {
      refreshing.value = false
    }
    showToast('加载失败')
  }
}

// 加载统计数据
const loadStats = async () => {
  // 获取所有猫咪用于统计（不带分页）
  const allCats = await catStore.fetchCats({ limit: 100 })
  const catsArray = Array.isArray(allCats) ? allCats : []

  totalCount.value = catsArray.length
  needHelpCount.value = catsArray.filter((c) => c.current_status === '需救助').length
  normalCount.value = catsArray.filter((c) => c.current_status === '正常').length
}

const onLoad = () => {
  loadCats()
}

const goToDetail = (id) => {
  router.push(`/cat/${id}`)
}

// 监听全局搜索事件
onMounted(() => {
  loadStats()
  window.addEventListener('global-search', handleGlobalSearch)
})

// 清理事件监听
import { onUnmounted } from 'vue'
onUnmounted(() => {
  window.removeEventListener('global-search', handleGlobalSearch)
})
</script>

<template>
  <div class="archive-view">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <van-search
        v-model="searchKeyword"
        placeholder="搜索猫咪..."
        shape="round"
        @search="onSearch"
        @clear="onSearch"
      />
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-item" @click="showCampusPicker = true">
        <span>{{ selectedCampus || '全部校区' }}</span>
        <van-icon name="arrow-down" />
      </div>
      <div class="filter-item" @click="showStatusPicker = true">
        <span>{{ selectedStatus || '全部状态' }}</span>
        <van-icon name="arrow-down" />
      </div>
      <div class="filter-item" @click="showGenderPicker = true">
        <span>{{ selectedGender || '全部性别' }}</span>
        <van-icon name="arrow-down" />
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card" @click="quickFilter('all')">
        <div class="stat-value">{{ totalCount }}</div>
        <div class="stat-label">猫咪总数</div>
      </div>
      <div class="stat-card" @click="quickFilter('需救助')">
        <div class="stat-value help">{{ needHelpCount }}</div>
        <div class="stat-label">需救助</div>
      </div>
      <div class="stat-card" @click="quickFilter('正常')">
        <div class="stat-value normal">{{ normalCount }}</div>
        <div class="stat-label">正常</div>
      </div>
    </div>

    <!-- 猫咪列表 -->
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多猫咪了"
        @load="onLoad"
        v-model:error="error"
        error-text="加载失败，点击重试"
      >
        <div class="cat-grid">
          <CatCard v-for="cat in catList" :key="cat.id" :cat="cat" @click="goToDetail(cat.id)" />
        </div>
        <EmptyState v-if="!loading && catList.length === 0" text="暂无猫咪" />
      </van-list>
    </van-pull-refresh>

    <!-- 校区选择器 -->
    <van-action-sheet v-model:show="showCampusPicker" title="选择校区">
      <div class="picker-content">
        <div
          v-for="campus in campusOptions"
          :key="campus.value"
          class="picker-item"
          :class="{ active: selectedCampus === campus.value }"
          @click="selectCampus(campus.value)"
        >
          {{ campus.label }}
        </div>
      </div>
    </van-action-sheet>

    <!-- 状态选择器 -->
    <van-action-sheet v-model:show="showStatusPicker" title="选择状态">
      <div class="picker-content">
        <div
          v-for="status in statusOptions"
          :key="status.value"
          class="picker-item"
          :class="{ active: selectedStatus === status.value }"
          @click="selectStatus(status.value)"
        >
          {{ status.label }}
        </div>
      </div>
    </van-action-sheet>

    <!-- 性别选择器 -->
    <van-action-sheet v-model:show="showGenderPicker" title="选择性别">
      <div class="picker-content">
        <div
          v-for="gender in genderOptions"
          :key="gender.value"
          class="picker-item"
          :class="{ active: selectedGender === gender.value }"
          @click="selectGender(gender.value)"
        >
          {{ gender.label }}
        </div>
      </div>
    </van-action-sheet>
  </div>
</template>

<style scoped lang="scss">
.archive-view {
  min-height: 100%;
  background: #f5f5f5;
}

.search-bar {
  background: white;
  padding: 8px 12px;
  position: sticky;
  top: 0;
  z-index: 99;
}

.filter-bar {
  display: flex;
  background: white;
  padding: 8px 16px;
  border-bottom: 1px solid #ebedf0;
  gap: 24px;

  .filter-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: #646566;
    cursor: pointer;
    padding: 4px 0;

    .van-icon {
      font-size: 12px;
    }

    &:active {
      opacity: 0.7;
    }
  }
}

.stats-cards {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  margin-bottom: 8px;

  .stat-card {
    flex: 1;
    text-align: center;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;

    &:active {
      transform: scale(0.96);
      background: #ebedf0;
    }

    .stat-value {
      font-size: 24px;
      font-weight: 700;
      color: #323233;

      &.help {
        color: #ff976a;
      }

      &.normal {
        color: #07c160;
      }
    }

    .stat-label {
      font-size: 12px;
      color: #969799;
      margin-top: 4px;
    }
  }
}

.cat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding: 12px;
}

.picker-content {
  padding: 12px 0;
  max-height: 50vh;
  overflow-y: auto;

  .picker-item {
    padding: 14px 20px;
    text-align: center;
    font-size: 15px;
    cursor: pointer;
    transition: background 0.2s;

    &:active {
      background: #f5f5f5;
    }

    &.active {
      color: #07c160;
      background: #e8f8f0;
    }
  }
}
</style>
