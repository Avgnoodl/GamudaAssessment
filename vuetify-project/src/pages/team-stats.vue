<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="font-bold">Team Stats</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4">
        <v-select
          v-model="team"
          clearable
          :items="teams"
          label="Select Team"
        />
      </v-col>
    </v-row>

    <v-row v-if="stats">
      <v-col cols="12" md="6">
        <v-table>
          <tbody>
            <tr>
              <th class="text-left">Played</th>
              <td>{{ stats.played }}</td>
            </tr>
            <tr>
              <th class="text-left">Wins</th>
              <td>{{ stats.wins }}</td>
            </tr>
            <tr>
              <th class="text-left">Draws</th>
              <td>{{ stats.draws }}</td>
            </tr>
            <tr>
              <th class="text-left">Losses</th>
              <td>{{ stats.losses }}</td>
            </tr>
            <tr>
              <th class="text-left">Goals For</th>
              <td>{{ stats.gf }}</td>
            </tr>
            <tr>
              <th class="text-left">Goals Against</th>
              <td>{{ stats.ga }}</td>
            </tr>
            <tr>
              <th class="text-left">Goal Difference</th>
              <td>{{ stats.gf - stats.ga }}</td>
            </tr>
            <tr>
              <th class="text-left">Points</th>
              <td>{{ stats.points }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'

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
    played: number
    wins: number
    draws: number
    losses: number
    gf: number
    ga: number
    points: number
  }

  const matches = ref<Match[]>([])
  const team = ref<string | null>(null)

  onMounted(async () => {
    const res = await fetch('http://localhost:8000/api/matches')
    matches.value = await res.json()
  })

  const teams = computed(() =>
    Array.from(new Set(matches.value.flatMap(m => [m.home_team, m.away_team]))).sort(),
  )

  const stats = computed<TeamStats | null>(() => {
    if (!team.value) return null
    const s: TeamStats = {
      played: 0,
      wins: 0,
      draws: 0,
      losses: 0,
      gf: 0,
      ga: 0,
      points: 0,
    }

    for (const m of matches.value) {
      let isHome: boolean | null = null
      if (m.home_team === team.value) isHome = true
      else if (m.away_team === team.value) isHome = false
      else continue

      s.played++
      const gf = isHome ? m.home_score : m.away_score
      const ga = isHome ? m.away_score : m.home_score
      s.gf += gf
      s.ga += ga

      if (gf > ga) {
        s.wins++
        s.points += 3
      } else if (gf < ga) {
        s.losses++
      } else {
        s.draws++
        s.points++
      }
    }

    return s
  })
</script>

<style scoped>
</style>

