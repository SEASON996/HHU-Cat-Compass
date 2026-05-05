<template>
  <div class="empty-state">
    <van-empty :image="image" :description="text">
      <template v-if="showButton" #description>
        <van-button v-if="showButton" type="primary" size="small" @click="$emit('action')">
          {{ buttonText }}
        </van-button>
      </template>
    </van-empty>
  </div>
</template>

<script setup>
defineProps({
  image: {
    type: String,
    default: 'search',
  },
  text: {
    type: String,
    default: '暂无数据',
  },
  showButton: {
    type: Boolean,
    default: false,
  },
  buttonText: {
    type: String,
    default: '重试',
  },
})

defineEmits(['action'])
</script>

<style scoped lang="scss">
.empty-state {
  padding: 60px 20px;
  text-align: center;
}
</style>
