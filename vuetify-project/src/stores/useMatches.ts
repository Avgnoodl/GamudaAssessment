import { defineStore } from 'pinia'
import axios from 'axios'

export const useMatches = defineStore('matches', {
  state: () => ({
    matches: [] as any[]   // type better later if you like
  }),

  actions: {
    async fetchAll () {
      const { data } = await axios.get('http://localhost:8000/api/matches')
      this.matches = data
    },

    startPolling () {
      this.fetchAll()                     // first load
      setInterval(this.fetchAll, 3000)   // every 1 s (HIGH FREQUENCY FOR SHOWCASE PURPOSES ONLY)
    }
  }
})
