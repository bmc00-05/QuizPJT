<template>
  <div>
    <h1>맵 페이지</h1>
    <ul>
      <li v-for="map in maps" :key="map.id">
        <RouterLink :to="{ name: 'stage', params: {'mapid':map.id}}" :map="map">
        {{ map.name }} - {{ map.description }}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const accountStore = useAccountStore()

const maps = ref([])

const getMaps = async () => {
  try {
    
    const res = await axios.get(
      'http://127.0.0.1:8000/api/v1/game/maps/',
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )

    maps.value = res.data

  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  getMaps()
})

</script>

<style scoped>

</style>