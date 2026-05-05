import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCats, getCatById, getCatRecords, getCatStats } from '@/api'

export const useCatStore = defineStore('cat', () => {
  const cats = ref([])
  const currentCat = ref(null)
  const records = ref([])
  const stats = ref(null)
  const loading = ref(false)
  const total = ref(0)

  // 获取猫咪列表
  const fetchCats = async (params = {}) => {
    loading.value = true
    try {
      const res = await getCats(params)
      cats.value = Array.isArray(res) ? res : []
      total.value = cats.value.length
      return cats.value
    } catch (error) {
      console.error('获取猫咪列表失败:', error)
      return []
    } finally {
      loading.value = false
    }
  }

  // 获取猫咪详情
  const fetchCatById = async (id) => {
    loading.value = true
    try {
      const res = await getCatById(id)
      currentCat.value = res
      return res
    } catch (error) {
      console.error('获取猫咪详情失败:', error)
      return null
    } finally {
      loading.value = false
    }
  }

  // 获取猫咪打卡记录
  const fetchCatRecords = async (catId, params = {}) => {
    try {
      const res = await getCatRecords(catId, params)
      records.value = Array.isArray(res) ? res : []
      return records.value
    } catch (error) {
      console.error('获取打卡记录失败:', error)
      records.value = []
      return []
    }
  }

  // 获取猫咪统计
  const fetchCatStats = async (catId) => {
    try {
      const res = await getCatStats(catId)
      stats.value = res
      return res
    } catch (error) {
      console.error('获取统计失败:', error)
      return null
    }
  }

  // 清除当前猫咪
  const clearCurrentCat = () => {
    currentCat.value = null
    records.value = []
    stats.value = null
  }

  return {
    cats,
    currentCat,
    records,
    stats,
    loading,
    total,
    fetchCats,
    fetchCatById,
    fetchCatRecords,
    fetchCatStats,
    clearCurrentCat,
  }
})
