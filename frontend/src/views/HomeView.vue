<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const startTest = () => {
  router.push('/quiz')
}
</script>

<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-br from-teal-500 to-blue-600 py-12 px-6 md:py-32 md:px-12 overflow-hidden">
      <!-- Decorative circle -->
      <div class="absolute -top-24 -right-24 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl"></div>

      <div class="max-w-4xl mx-auto text-center relative z-10">
        <div class="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-md px-4 py-2 rounded-full text-white text-sm font-medium mb-8">
          <span class="flex h-2 w-2 rounded-full bg-red-400 animate-pulse"></span>
          <span>今日已有 129,482 人完成测试</span>
        </div>
        
        <h1 class="text-3xl sm:text-4xl md:text-6xl font-extrabold text-white mb-6 leading-tight">
          通过性格色彩，<br/><span class="text-teal-100">遇见最真实的自己</span>
        </h1>
        
        <p class="text-base sm:text-lg md:text-xl text-blue-50 mb-10 md:mb-12 max-w-2xl mx-auto leading-relaxed">
          基于乐嘉性格色彩心理学，深入剖析您的核心动机，<br/>
          帮助您在职场、人际关系与自我认知中获得洞察。
        </p>
        
        <button 
          @click="startTest"
          class="bg-white text-blue-600 hover:bg-blue-50 text-lg md:text-xl font-bold py-4 px-10 md:py-5 md:px-12 rounded-full shadow-2xl transition-all hover:scale-105 active:scale-95 w-full sm:w-auto"
        >
          立即开始测试
        </button>
      </div>
    </section>

    <!-- Trust Stats -->
    <section class="py-12 bg-slate-50 border-y border-slate-100">
      <div class="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 px-4">
        <div class="text-center">
          <div class="text-3xl font-bold text-slate-800">98.2%</div>
          <div class="text-slate-500 text-sm">用户满意度</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-slate-800">30 道</div>
          <div class="text-slate-500 text-sm">精选试题</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-slate-800">专业级</div>
          <div class="text-slate-500 text-sm">测评体系</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-slate-800">2 min</div>
          <div class="text-slate-500 text-sm">平均完成时间</div>
        </div>
      </div>
    </section>

    <!-- Content Sections -->
    <section class="py-20 px-4">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-slate-800 mb-16">为什么选择性格色彩测试？</h2>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
            <div class="w-14 h-14 bg-red-100 rounded-2xl flex items-center justify-center mb-6 text-red-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-4 text-slate-800">洞察核心动机</h3>
            <p class="text-slate-500 leading-relaxed">不仅仅关注行为，更深入探索行为背后的心理动机，解答“我为什么会这样做”。</p>
          </div>

          <div class="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
            <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center mb-6 text-blue-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 005.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-4 text-slate-800">改善人际关系</h3>
            <p class="text-slate-500 leading-relaxed">理解他人，包容差异。学会与不同“颜色”的人高效沟通，减少冲突。</p>
          </div>

          <div class="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
            <div class="w-14 h-14 bg-yellow-100 rounded-2xl flex items-center justify-center mb-6 text-yellow-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-4 text-slate-800">实现职业进阶</h3>
            <p class="text-slate-500 leading-relaxed">明确性格优势，找到最适合自己的岗位，避开性格短板带来的职业困扰。</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 border-t border-slate-100 text-center text-slate-400 text-sm">
      © 2026 ColorQA 专业心理测评
    </footer>
  </div>
</template>
