<template>
  <v-container>
    <h1 class="font-bold mb-4">League Table</h1>

    <!-- League selector -->
    <v-row dense class="mb-2" align="center">
      <v-col cols="auto" style="min-width:200px">
        <v-select
          v-model="leagueFilter"
          :items="['All', ...leagues]"
          label="Select league"
          density="compact"
          hide-details
          clearable
        />
      </v-col>
    </v-row>

    <v-slide-y-transition group>
      <v-data-table
        :headers="headers"
        :items="table"
        item-key="name"
        class="elevation-1"
        density="compact"
        :sort-by="[{ key: 'points', order: 'desc' }]"
        mobile-breakpoint="600"
        @click:row="openTeam"
      >
        <!-- rank with colour bands -->
        <template #item.rank="{ item }">
          <v-chip
            :color="item.rank <= 4 ? 'green' : item.rank >= table.length - 2 ? 'red' : 'grey'"
            size="x-small"
            class="text-white w-100 justify-center"
          >
            {{ item.rank }}
          </v-chip>
        </template>

        <!-- team avatar + name -->
        <template #item.name="{ item }">
          <div class="d-flex align-center gap-2">
            <v-avatar size="24">
              <img :src="`/team-logos/${item.name}.png`" alt="" />
            </v-avatar>
            {{ item.name }}
          </div>
        </template>

        <!-- last-5 form dots -->
        <template #item.form="{ item }">
          <div class="d-flex gap-1">
            <v-icon v-for="(r,i) in item.form" :key="i" size="16"
              :color="r==='W' ? 'green' : r==='L' ? 'red' : 'grey'">
              mdi-circle-medium
            </v-icon>
          </div>
        </template>

        <!-- points progress bar -->
        <template #item.points="{ item }">
          <v-progress-linear
            :model-value="(item.points / maxPoints) * 100"
            height="8"
            rounded
            color="primary"
          />
          <span class="ms-2">{{ item.points }}</span>
        </template>
      </v-data-table>
    </v-slide-y-transition>

    <!-- team detail drawer -->
    <v-navigation-drawer v-model="drawer" right temporary width="300">
      <template #default>
        <v-list-subheader>{{ selectedTeam?.name }}</v-list-subheader>
        <!-- recent matches, squad, etc. -->
      </template>
    </v-navigation-drawer>
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
  gd: number
  rank: number
  ppg: number
  winRate: number
  form: string[]
}

const matches = ref<Match[]>([])
const drawer = ref(false)
const selectedTeam = ref<TeamRow | null>(null)
const leagueFilter = ref<string>('All')

function openTeam(team: TeamRow) {
  selectedTeam.value = team
  drawer.value = true
}

onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/matches')
  matches.value = await res.json()
})

const leagues = computed(() => [...new Set(matches.value.map(m => m.league))].sort())

const filteredMatches = computed(() =>
  leagueFilter.value === 'All' ? matches.value : matches.value.filter(m => m.league === leagueFilter.value)
)

const table = computed<TeamRow[]>(() => {
  const map = new Map<string, TeamRow>()
  const lastFive: Record<string, string[]> = {}

  for (const m of filteredMatches.value) {
    const init = (name: string) =>
      map.get(name) || {
        name,
        played: 0,
        wins: 0,
        draws: 0,
        losses: 0,
        gf: 0,
        ga: 0,
        points: 0,
        gd: 0,
        rank: 0,
        ppg: 0,
        winRate: 0,
        form: []
      }

    const home = init(m.home_team)
    const away = init(m.away_team)

    home.played++
    away.played++
    home.gf += m.home_score
    home.ga += m.away_score
    away.gf += m.away_score
    away.ga += m.home_score

    if (m.home_score > m.away_score) {
      home.wins++; home.points += 3; away.losses++;
      lastFive[m.home_team] = [...(lastFive[m.home_team] || []), 'W']
      lastFive[m.away_team] = [...(lastFive[m.away_team] || []), 'L']
    } else if (m.home_score < m.away_score) {
      away.wins++; away.points += 3; home.losses++;
      lastFive[m.away_team] = [...(lastFive[m.away_team] || []), 'W']
      lastFive[m.home_team] = [...(lastFive[m.home_team] || []), 'L']
    } else {
      home.draws++; away.draws++; home.points++; away.points++;
      lastFive[m.home_team] = [...(lastFive[m.home_team] || []), 'D']
      lastFive[m.away_team] = [...(lastFive[m.away_team] || []), 'D']
    }

    map.set(home.name, home)
    map.set(away.name, away)
  }

  const arr = Array.from(map.values()).map(t => {
    t.gd = t.gf - t.ga
    t.ppg = parseFloat((t.points / t.played).toFixed(2))
    t.winRate = parseFloat(((t.wins / t.played) * 100).toFixed(0))
    t.form = (lastFive[t.name] || []).slice(-5).reverse()
    return t
  }).sort((a, b) => {
    if (b.points !== a.points) return b.points - a.points
    if (b.gd !== a.gd) return b.gd - a.gd
    return b.gf - a.gf
  })

  arr.forEach((t, i) => (t.rank = i + 1))
  return arr
})

const maxPoints = computed(() => table.value[0]?.points || 0)

const headers = [
  { title: '#', value: 'rank', width: 56 },
  { title: 'Team', value: 'name' },
  { title: 'P', value: 'played' },
  { title: 'W', value: 'wins' },
  { title: 'D', value: 'draws' },
  { title: 'L', value: 'losses' },
  { title: 'GF', value: 'gf', class: 'd-none d-sm-table-cell' },
  { title: 'GA', value: 'ga', class: 'd-none d-sm-table-cell' },
  { title: 'GD', value: 'gd', class: 'd-none d-sm-table-cell' },
  { title: 'PPG', value: 'ppg', class: 'd-none d-md-table-cell' },
  { title: 'Win%', value: 'winRate', class: 'd-none d-md-table-cell' },
  { title: 'Form', value: 'form', sortable: false },
  { title: 'Pts', value: 'points' }
]
</script>

<style scoped>
.v-data-table thead th {
  font-weight: 600;
  background: rgba(var(--v-theme-primary), 0.08);
}

.v-data-table tbody tr:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  cursor: pointer;
}
</style>
