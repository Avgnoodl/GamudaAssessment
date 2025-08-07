import axios from 'axios'
import { defineStore } from 'pinia'

export interface MatchEvent {
  minute: number
  team: string
  player: string
  type: string
  sub_in?: string | null
}

export interface Match {
  id: number
  league: string
  home_team: string
  away_team: string
  home_score: number
  away_score: number
  kickoff_time: string
  status: string
  events: MatchEvent[]
  current_minute?: number | null
}

let poll: number | null = null
let ws: WebSocket | null = null

export const useMatches = defineStore('matches', {
  state: () => ({
    matches: [] as Match[],
  }),
  actions: {
    async fetchAll () {
      const { data } = await axios.get('/api/matches')
      this.matches = data
    },
    startPolling () {
      this.fetchAll()
      if (poll) {
        clearInterval(poll)
      }
      poll = setInterval(() => this.fetchAll(), 10_000)
    },
    connectWS () {
      if (ws) {
        ws.close()
      }
      const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
      ws = new WebSocket(`${protocol}://${window.location.host}/ws/matches`)
      ws.addEventListener('message', e => {
        this.matches = JSON.parse(e.data)
      })
    },
  },
})
