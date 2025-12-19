import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  
  const API_URL = 'http://127.0.0.1:8000/api/v1/'

  const getMaps = async () => {

  try {
    const res = await axios.get(
      `${API_URL}/accounts/signup/`
    )
    return res

  } catch (err) {
    throw err
  }
  }

})
