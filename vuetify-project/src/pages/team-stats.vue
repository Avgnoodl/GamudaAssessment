<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="font-bold">Team Stats</h1>
      </v-col>
    </v-row>

    <!-- Cards grid -->
    <v-row class="mt-4">
      <v-col
        v-for="teamStat in table"
        :key="teamStat.name"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="pa-4 mb-4 match-card">
          <v-card-title class="text-h6">{{ teamStat.name }}</v-card-title>
          <v-card-subtitle>
            Played: {{ teamStat.played }} |
            Wins: {{ teamStat.wins }} |
            Draws: {{ teamStat.draws }} |
            Losses: {{ teamStat.losses }}
          </v-card-subtitle>
          <v-card-text>
            Goals For: {{ teamStat.gf }} |
            Goals Against: {{ teamStat.ga }} |
            Points: {{ teamStat.points }}
          </v-card-text>
          <v-card-actions>
            <v-btn
              @click="$router.push(`/team/${encodeURIComponent(teamStat.name)}`)"
              color="primary"
              block
              :disabled="true"
            >
              View Matches
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Match {
  id: number
  league: string
  home_team: string
  away_team: string
  home_score: number
  away_score: number
  kickoff_time: string
  status: string
}

interface TeamStats {
  name: string
  played: number
  wins: number
  draws: number
  losses: number
  gf: number
  ga: number
  points: number
}

const matches = ref<Match[]>([])

onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/matches')
  matches.value = await res.json()
})

// list of unique team names
const teamNames = computed(() =>
  Array.from(
    new Set(matches.value.flatMap(m => [m.home_team, m.away_team]))
  ).sort()
)

// build stats for each team
const table = computed<TeamStats[]>(() => {
  return teamNames.value.map(name => {
    const stats: TeamStats = {
      name,
      played: 0,
      wins: 0,
      draws: 0,
      losses: 0,
      gf: 0,
      ga: 0,
      points: 0
    }

    for (const m of matches.value) {
      let isHome: boolean | null = null
      if (m.home_team === name) isHome = true
      else if (m.away_team === name) isHome = false
      else continue

      stats.played++
      const gf = isHome ? m.home_score : m.away_score
      const ga = isHome ? m.away_score : m.home_score
      stats.gf += gf
      stats.ga += ga

      if (gf > ga) {
        stats.wins++
        stats.points += 3
      } else if (gf < ga) {
        stats.losses++
      } else {
        stats.draws++
        stats.points += 1
      }
    }

    return stats
  })
})
</script>

<style scoped>
/* if you want cards to all stretch to same height: */
.v-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
