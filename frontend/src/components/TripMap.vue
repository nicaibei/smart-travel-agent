<template>
  <a-card title="景点地图" :bordered="false" class="map-card">
    <div v-if="locations.length" class="map-layout">
      <iframe class="map-frame" :src="mapUrl" title="旅行景点地图" loading="lazy" />
      <div class="map-legend">
        <div v-for="(location, index) in locations" :key="`${location.name}-${index}`" class="map-place">
          <span class="map-index">{{ index + 1 }}</span>
          <div><strong>{{ location.name }}</strong><small>{{ location.address }}</small></div>
        </div>
      </div>
    </div>
    <a-empty v-else description="暂无可定位的景点" />
  </a-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { TripPlan } from '@/types';

const props = defineProps<{ tripPlan: TripPlan }>();
const locations = computed(() => props.tripPlan.days.flatMap(day =>
  day.attractions.filter(item => item.location).map(item => ({
    name: item.name, address: item.address,
    latitude: item.location.latitude, longitude: item.location.longitude,
  }))
).slice(0, 20));
const mapUrl = computed(() => {
  const first = locations.value[0];
  const lats = locations.value.map(item => item.latitude);
  const lngs = locations.value.map(item => item.longitude);
  const padding = 0.03;
  const bbox = `${Math.min(...lngs) - padding},${Math.min(...lats) - padding},${Math.max(...lngs) + padding},${Math.max(...lats) + padding}`;
  return `https://www.openstreetmap.org/export/embed.html?bbox=${encodeURIComponent(bbox)}&layer=mapnik&marker=${first.latitude},${first.longitude}`;
});
</script>

<style scoped>
.map-card { margin: 24px 0; }
.map-layout { display: grid; grid-template-columns: minmax(0, 2fr) minmax(220px, 1fr); gap: 16px; }
.map-frame { width: 100%; min-height: 360px; border: 0; border-radius: 8px; }
.map-legend { max-height: 360px; overflow: auto; }
.map-place { display: flex; gap: 10px; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.map-index { flex: 0 0 24px; height: 24px; border-radius: 50%; background: #1677ff; color: white; text-align: center; line-height: 24px; }
.map-place small { display: block; margin-top: 4px; color: #888; }
@media (max-width: 768px) { .map-layout { grid-template-columns: 1fr; } }
</style>
