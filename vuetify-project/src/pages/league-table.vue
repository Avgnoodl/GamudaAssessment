<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="font-bold">League Table</h1>
        <v-table class="mt-4">
          <thead>
            <tr>
              <th>#</th>
              <th>Team</th>
              <th>P</th>
              <th>W</th>
              <th>D</th>
              <th>L</th>
              <th>GF</th>
              <th>GA</th>
              <th>GD</th>
              <th>Pts</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(team, i) in table" :key="team.name">
              <td>{{ i + 1 }}</td>
              <td>{{ team.name }}</td>
              <td>{{ team.played }}</td>
              <td>{{ team.wins }}</td>
              <td>{{ team.draws }}</td>
              <td>{{ team.losses }}</td>
              <td>{{ team.gf }}</td>
              <td>{{ team.ga }}</td>
              <td>{{ team.gf - team.ga }}</td>
              <td>{{ team.points }}</td>
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

  interface TeamRow {
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

  const table = computed<TeamRow[]>(() => {
    const map = new Map<string, TeamRow>()

    for (const m of matches.value) {
      const home = map.get(m.home_team) || { name: m.home_team, played: 0, wins: 0, draws: 0, losses: 0, gf: 0, ga: 0, points: 0 }
      const away = map.get(m.away_team) || { name: m.away_team, played: 0, wins: 0, draws: 0, losses: 0, gf: 0, ga: 0, points: 0 }

      home.played++
      away.played++
      home.gf += m.home_score
      home.ga += m.away_score
      away.gf += m.away_score
      away.ga += m.home_score

      if (m.home_score > m.away_score) {
        home.wins++
        home.points += 3
        away.losses++
      } else if (m.home_score < m.away_score) {
        away.wins++
        away.points += 3
        home.losses++
      } else {
        home.draws++
        away.draws++
        home.points++
        away.points++
      }

      map.set(home.name, home)
      map.set(away.name, away)
    }

    return Array.from(map.values()).sort((a, b) => {
      if (b.points !== a.points) return b.points - a.points
      const gdA = a.gf - a.ga
      const gdB = b.gf - b.ga
      if (gdB !== gdA) return gdB - gdA
      return b.gf - a.gf
    })
  })
</script>

<style scoped>
</style>

