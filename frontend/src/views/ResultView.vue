<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTestStore } from '../stores/test'
import axios from 'axios'

const router = useRouter()
const store = useTestStore()
const config = ref(null)
const loading = ref(true)

const API_BASE = "/api"

onMounted(async () => {
  if (!store.results) {
    router.push('/')
    return
  }
  
  try {
    const response = await axios.get(`${API_BASE}/questions/config/${store.results.final_color}`)
    config.value = response.data
  } catch (error) {
    console.error("Failed to load personality config:", error)
  } finally {
    loading.value = false
  }
})

const colorTheme = {
  red: { bg: 'bg-red-500', text: 'text-red-600', ring: 'ring-red-100', light: 'bg-red-50' },
  blue: { bg: 'bg-blue-500', text: 'text-blue-600', ring: 'ring-blue-100', light: 'bg-blue-50' },
  yellow: { bg: 'bg-yellow-500', text: 'text-yellow-600', ring: 'ring-yellow-100', light: 'bg-yellow-50' },
  green: { bg: 'bg-green-500', text: 'text-green-600', ring: 'ring-green-100', light: 'bg-green-50' }
}

const currentTheme = computed(() => colorTheme[store.results?.final_color] || colorTheme.blue)

// Parse the detailed description into sections
const sections = computed(() => {
  if (!config.value?.description) return []
  return config.value.description.split('\n\n').map(s => {
    const parts = s.split('】')
    return {
      title: parts[0].replace('【', ''),
      content: parts[1] || s
    }
  })
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 py-8 px-4 sm:py-16">
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>

    <div v-else-if="config" class="max-w-4xl mx-auto">
      <div class="bg-white rounded-[2rem] shadow-2xl overflow-hidden border border-slate-100 transition-all duration-700">
        <!-- Premium Header -->
        <div :class="['relative py-16 px-8 text-center text-white overflow-hidden', currentTheme.bg]">
          <div class="absolute inset-0 bg-black/10"></div>
          <div class="absolute -top-24 -right-24 w-64 h-64 bg-white/20 rounded-full blur-3xl"></div>
          <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-black/10 rounded-full blur-3xl"></div>
          
          <div class="relative z-10">
            <div class="inline-block px-4 py-1 rounded-full bg-white/20 backdrop-blur-md text-sm font-bold mb-4">
              测评报告已生成
            </div>
            <h1 class="text-4xl md:text-5xl font-black mb-4 tracking-tight">{{ config.title }}</h1>
            <p class="text-white/90 text-lg md:text-xl font-medium">{{ config.subtitle }}</p>
          </div>
        </div>

        <!-- Scoring Visualization -->
        <div class="p-8 md:p-12">
          <div class="flex flex-col md:flex-row items-center gap-12">
            <div class="w-full md:w-1/2">
              <h3 class="text-xl font-bold text-slate-800 mb-8 flex items-center">
                <span class="w-2 h-6 bg-indigo-600 rounded-full mr-3"></span>
                色彩维度分布
              </h3>
              <div class="space-y-6">
                <div v-for="(score, color) in store.results.scores" :key="color" class="group">
                  <div class="flex justify-between mb-2">
                    <span class="text-sm font-bold text-slate-500 uppercase tracking-wider">{{ color }}</span>
                    <span class="text-sm font-black text-slate-800">{{ score }} / 30</span>
                  </div>
                  <div class="h-3 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      :class="['h-full transition-all duration-1000 ease-out', colorTheme[color].bg]"
                      :style="{ width: `${(score / 30) * 100}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="w-full md:w-1/2 flex justify-center">
              <div :class="['w-48 h-48 rounded-full flex flex-col items-center justify-center border-8 shadow-inner transition-transform hover:scale-105', currentTheme.ring, currentTheme.light]">
                <span class="text-sm font-bold text-slate-400">主色调</span>
                <span :class="['text-3xl font-black', currentTheme.text]">{{ store.results.final_color.toUpperCase() }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Analysis Sections -->
        <div class="px-8 md:px-12 pb-12 grid gap-6 md:grid-cols-2">
          <div 
            v-for="section in sections" 
            :key="section.title"
            class="p-8 rounded-3xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-xl hover:border-indigo-100 transition-all duration-300 group"
          >
            <div class="flex items-center mb-4">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform', currentTheme.bg, 'text-white']">
                <svg v-if="section.title.includes('性格')" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <svg v-else-if="section.title.includes('优势')" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else-if="section.title.includes('局限')" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h4 class="text-xl font-bold text-slate-800">{{ section.title }}</h4>
            </div>
            <p class="text-slate-600 leading-relaxed whitespace-pre-wrap">
              {{ section.content }}
            </p>
          </div>
        </div>

        <!-- Final CTA -->
        <div class="p-12 bg-slate-50 text-center border-t border-slate-100">
          <div class="mb-8">
            <h5 class="text-slate-800 font-bold mb-2">想了解更多？</h5>
            <p class="text-slate-500">邀请好友测试，探索你们的性格火花</p>
          </div>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <button 
              @click="router.push('/')"
              class="bg-indigo-600 text-white font-bold py-4 px-12 rounded-full hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all hover:-translate-y-1"
            >
              再测一次
            </button>
            <button 
              class="bg-white text-slate-700 border border-slate-200 font-bold py-4 px-12 rounded-full hover:bg-slate-50 transition-all"
            >
              保存报告
            </button>
          </div>
        </div>
      </div>
      
      <!-- Footer Copyright -->
      <p class="mt-12 text-center text-slate-400 text-sm">
        ColorQA 测评系统提供技术支持 &copy; 2026
      </p>
    </div>
  </div>
</template>

<style scoped>
.prose {
  max-width: 65ch;
}
</style>
