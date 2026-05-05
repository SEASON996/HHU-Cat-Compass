<template>
  <div class="cat-card" @click="$emit('click')">
    <div class="card-image">
      <img :src="cat.photo_url" :alt="cat.name" @error="handleImageError" />
      <span class="status-badge" :class="statusClass">{{ cat.current_status }}</span>
    </div>
    <div class="card-info">
      <h3 class="cat-name">{{ cat.name }}</h3>
      <p class="cat-meta">
        <span>{{ cat.gender }}</span>
        <span>·</span>
        <span>{{ cat.age_stage }}</span>
      </p>
      <p class="cat-location">
        <van-icon name="location-o" />
        <span>{{ truncate(cat.location_desc, 12) }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  cat: {
    type: Object,
    required: true,
  },
})

defineEmits(['click'])

const statusClass = computed(() => {
  const statusMap = {
    正常: 'status-normal',
    需救助: 'status-help',
    已绝育: 'status-neutered',
    已领养: 'status-adopted',
    失踪: 'status-missing',
  }
  return statusMap[props.cat.current_status] || ''
})

const defaultImage = `data:image/svg+xml,${encodeURIComponent(`
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <rect width="200" height="200" fill="#f0f0f0"/>
    <text x="100" y="120" text-anchor="middle" font-size="64" fill="#bbb">🐱</text>
    <text x="100" y="170" text-anchor="middle" font-size="24" fill="#aaa">暂无照片</text>
  </svg>
`)}`

const handleImageError = (e) => {
  if (e.target.src !== defaultImage) {
    e.target.src = defaultImage
  }
}

const truncate = (str, length) => {
  if (!str) return ''
  if (str.length <= length) return str
  return str.slice(0, length) + '...'
}
</script>

<style scoped lang="scss">
.cat-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s;
  cursor: pointer;

  &:active {
    transform: scale(0.98);
  }

  .card-image {
    position: relative;
    aspect-ratio: 1;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .status-badge {
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 4px 8px;
      border-radius: 12px;
      font-size: 11px;
      color: white;
      font-weight: 500;

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

  .card-info {
    padding: 10px;

    .cat-name {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 4px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .cat-meta {
      font-size: 12px;
      color: #969799;
      margin-bottom: 6px;

      span {
        margin-right: 4px;
      }
    }

    .cat-location {
      font-size: 11px;
      color: #969799;
      display: flex;
      align-items: center;
      gap: 4px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;

      .van-icon {
        font-size: 12px;
        flex-shrink: 0;
      }

      span {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
  }
}
</style>
