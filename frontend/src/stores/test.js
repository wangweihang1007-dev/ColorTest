import { defineStore } from 'pinia'

export const useTestStore = defineStore('test', {
  state: () => ({
    user: null,
    questions: [],
    answers: [], // [{q_id: 1, opt_id: 1}]
    results: null
  }),
  actions: {
    setQuestions(qs) {
      this.questions = qs
    },
    saveAnswer(q_id, opt_id) {
      const index = this.answers.findIndex(a => a.q_id === q_id)
      if (index > -1) {
        this.answers[index].opt_id = opt_id
      } else {
        this.answers.push({ q_id, opt_id })
      }
    }
  }
})
