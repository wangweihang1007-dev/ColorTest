<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useTestStore } from '../stores/test'

const router = useRouter()
const store = useTestStore()
const currentIndex = ref(0)
const selectedOption = ref(null)
const questions = ref([])
const loading = ref(true)

const API_BASE = "/api"

onMounted(async () => {
  try {
    const response = await axios.get(`${API_BASE}/questions/`)
    questions.value = response.data
    store.setQuestions(response.data)
  } catch (error) {
    console.error("Failed to load questions:", error)
    alert("题库加载失败，请检查后端服务是否启动。")
  } finally {
    loading.value = false
  }
})

const progress = computed(() => {
  if (questions.value.length === 0) return 0
  return ((currentIndex.value) / questions.value.length) * 100
})

const handleSelect = async (optionId) => {
  selectedOption.value = optionId
  
  // Save to Pinia
  store.saveAnswer(questions.value[currentIndex.value].id, optionId)

  setTimeout(async () => {
    if (currentIndex.value < questions.value.length - 1) {
      currentIndex.value++
      selectedOption.value = null
    } else {
      // Submit results
      try {
        const res = await axios.post(`${API_BASE}/records/submit`, {
          user_id: 1, // Currently hardcoded for demo
          answers: store.answers
        })
        store.results = res.data
        router.push('/result')
      } catch (error) {
        console.error("Submission failed:", error)
        alert("结果提交失败")
      }
    }
  }, 300)
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex flex-col items-center py-6 px-4 sm:py-12 sm:px-6 font-sans">
    <!-- Progress Bar -->
    <div class="w-full max-w-2xl bg-gray-200 h-2 rounded-full mb-12 overflow-hidden">
      <div 
        class="bg-indigo-600 h-full transition-all duration-500 ease-out"
        :style="{ width: `${progress}%` }"
      ></div>
    </div>

    <!-- Question Container -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
      <p class="text-slate-500">正在加载精选题库...</p>
    </div>

    <div v-else-if="questions.length > 0" class="w-full max-w-2xl px-2 sm:px-0">
      <transition name="fade" mode="out-in">
        <div :key="currentIndex" class="bg-white rounded-2xl sm:rounded-3xl shadow-xl shadow-slate-200/60 p-6 md:p-12 border border-slate-100">
          <div class="text-indigo-600 font-bold mb-4 tracking-widest uppercase text-sm">
            Question {{ currentIndex + 1 }} / {{ questions.length }}
          </div>
          
          <h2 class="text-2xl md:text-3xl font-bold text-slate-800 mb-10 leading-tight">
            {{ questions[currentIndex]?.content }}
          </h2>

          <div class="space-y-4">
            <button 
              v-for="opt in questions[currentIndex].options" 
              :key="opt.id"
              @click="handleSelect(opt.id)"
              :class="[
                'w-full text-left p-4 sm:p-6 rounded-xl sm:rounded-2xl border-2 transition-all duration-200 group relative overflow-hidden',
                selectedOption === opt.id 
                  ? 'border-indigo-600 bg-indigo-50 shadow-md transform scale-[1.02]' 
                  : 'border-slate-100 hover:border-indigo-200 hover:bg-slate-50'
              ]"
            >
              <div class="flex items-center">
                <span :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center font-bold mr-4 transition-colors',
                  selectedOption === opt.id ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-500 group-hover:bg-indigo-100'
                ]">
                  {{ opt.label }}
                </span>
                <span class="text-lg text-slate-700 font-medium leading-snug">{{ opt.content }}</span>
              </div>
            </button>
          </div>
        </div>
      </transition>
    </div>

    <div v-else class="text-center py-20">
      <p class="text-slate-500 mb-4">暂无题目数据</p>
      <button @click="router.push('/')" class="text-indigo-600 font-bold">返回首页</button>
    </div>

    <!-- Footer Info -->
    <div class="mt-8 text-slate-400 text-sm">
      请选择最符合您的选项
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
