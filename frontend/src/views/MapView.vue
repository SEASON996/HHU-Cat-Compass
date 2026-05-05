<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCatStore } from '@/stores/cat'
import { useUserStore } from '@/stores/user'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import EncounterCat from '@/components/EncounterCat.vue'

const router = useRouter()
const catStore = useCatStore()
const userStore = useUserStore()

const mapRef = ref(null)
let map = null
let markers = []

const currentCampus = ref('江宁')

const showPopup = ref(false)

const campuses = [
  { label: '江宁', value: '江宁', center: [31.9111, 118.7891] },
  { label: '西康路', value: '西康路', center: [32.0567, 118.7654] },
  { label: '金坛', value: '金坛', center: [31.7534, 119.5678] },
]

const campusCenters = {
  江宁: [31.9111, 118.7891],
  西康路: [32.0567, 118.7654],
  金坛: [31.7534, 119.5678],
}

// 初始化地图
const initMap = () => {
  if (!mapRef.value) return

  map = L.map(mapRef.value).setView(campusCenters[currentCampus.value], 15)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  // 地图大小变化时刷新
  setTimeout(() => {
    if (map) map.invalidateSize()
  }, 100)
}

// 添加猫咪标记
const addCatMarkers = (cats) => {
  if (!map) return

  markers.forEach((marker) => {
    if (marker && marker.remove) marker.remove()
  })
  markers = []

  cats.forEach((cat) => {
    const marker = L.marker([cat.latitude, cat.longitude]).addTo(map).bindPopup(`
        <div style="text-align: center; min-width: 120px;">
          <strong>${cat.name}</strong><br/>
          ${cat.location_desc}<br/>
          <button onclick="window.viewCatDetail('${cat.id}')" style="margin-top: 5px; padding: 2px 12px; background: #07c160; color: white; border: none; border-radius: 4px; cursor: pointer;">查看详情</button>
        </div>
      `)

    markers.push(marker)
  })
}

// 加载猫咪数据
const loadCats = async () => {
  await catStore.fetchCats({ campus: currentCampus.value })
  addCatMarkers(catStore.cats)
}

// 切换校区
const onCampusChange = async (campus) => {
  currentCampus.value = campus
  if (map) {
    map.setView(campusCenters[campus], 15)
  }
  await loadCats()
}

// 定位到用户当前位置
const centerToUserLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords
        if (map) {
          map.setView([latitude, longitude], 15)
        }
      },
      (error) => {
        console.error('定位失败:', error)
      },
    )
  }
}

// 全局函数用于 popup 跳转
window.viewCatDetail = (id) => {
  router.push(`/cat/${id}`)
}

// 打卡成功后的回调, 刷新数据
const handleSuccess = () => {
  // 可选：刷新地图标记或猫咪统计
  loadCats()
}

onMounted(async () => {
  await new Promise((resolve) => setTimeout(resolve, 100))
  initMap()
  await loadCats()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
  delete window.viewCatDetail
})
</script>

<template>
  <div class="map-view">
    <!-- 校区切换器 -->
    <div class="campus-tabs">
      <div
        v-for="campus in campuses"
        :key="campus.value"
        class="campus-tab"
        :class="{ active: currentCampus === campus.value }"
        @click="onCampusChange(campus.value)"
      >
        {{ campus.label }}
      </div>
    </div>

    <!-- 地图容器 -->
    <div class="map-container">
      <div ref="mapRef" class="map"></div>
    </div>

    <!-- 右下角定位按钮 -->
    <div class="location-btn" @click="centerToUserLocation">
      <van-icon name="aim" />
    </div>

    <!-- 偶遇打卡按钮 -->
    <div class="encounter-btn" @click="showPopup = true">
      <van-icon name="camera-o" />
      <span>偶遇打卡</span>
    </div>

    <encounter-cat
      v-model:visible="showPopup"
      :cats="catStore.cats"
      :user-id="userStore.userId"
      @success="handleSuccess"
    />
  </div>
</template>

<style scoped lang="scss">
.map-view {
  width: 100%;
  height: 100%;
  position: relative; // 为绝对定位的子元素提供参考
}

.campus-tabs {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.95);
  padding: 6px 12px;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;

  .campus-tab {
    padding: 6px 16px;
    font-size: 14px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;

    &.active {
      background: #07c160;
      color: white;
    }

    &:active {
      transform: scale(0.95);
    }
  }
}

.map-container {
  width: 100%;
  height: 100%;

  .map {
    width: 100%;
    height: 100%;
    z-index: 1;
  }
}

.location-btn {
  position: absolute;
  bottom: 16px;
  right: 16px;
  width: 44px;
  height: 44px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  z-index: 10;

  &:active {
    transform: scale(0.95);
  }

  .van-icon {
    font-size: 20px;
    color: #07c160;
  }
}

.encounter-btn {
  position: absolute;
  bottom: 60px;
  transform: translateX(-50%);
  left: 50%;
  display: flex;
  align-items: center;
  gap: 6px;
  background: #07c160;
  color: white;
  padding: 10px 20px;
  border-radius: 40px;
  box-shadow: 0 2px 12px rgba(7, 193, 96, 0.3);
  cursor: pointer;
  z-index: 10;
  font-size: 14px;
  font-weight: 500;

  .van-icon {
    font-size: 18px;
  }
}
</style>
