<template>
  <div>
    <h1>문제집 생성 페이지</h1>
  </div>

      <div class="mt-8">
        <form @submit.prevent="createProblemSets" class="space-y-6">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-900">
              Title
            </label>
            <div class="mt-2">
              <input
                v-model.trim="title"
                id="title"
                type="text"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>
          <div>
            <label for="description" class="block text-sm font-medium text-gray-900">
              Description
            </label>
            <div class="mt-2">
              <input
                v-model.trim="description"
                id="description"
                type="text"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>
          <button
            type="submit"
            class="w-full rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
          >
            문제집 생성
          </button>
        </form>
      </div>

      <div>
        <h2>생성 정보</h2>
        {{ problemSet }}
      </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts'
  import { useRouter } from 'vue-router'
  import axios from 'axios'

  const accountStore = useAccountStore()

  const problemSet = ref(null)
  const title = ref(null)
  const description = ref(null)

const createProblemSets = async () => {
  try {
    
    const res = await axios.post(
      `http://127.0.0.1:8000/api/v1/questions/problemsets/`,
      {
        title: title.value,
        description: description.value
      },
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )

    problemSet.value = res.data

  } catch (err) {
    console.error(err)
  }
}
</script>

<style scoped>

</style>