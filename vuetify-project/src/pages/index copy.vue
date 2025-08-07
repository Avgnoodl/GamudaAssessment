<template>
  <v-container>
    <!-- Header -->
    <v-row>
      <v-col class="text-h4 mb-4">
        Football Match Dashboard
      </v-col>
    </v-row>

    <!-- Filters Row -->
    <v-row align="center" class="mb-4">
      <v-spacer />

      <!-- League filter -->
      <v-col cols="auto" style="min-width:200px">
        <v-select
          v-model="league"
          clearable
          :items="leagues"
          label="Filter by league"
          style="max-width:250px"
        />
      </v-col>
      <v-col cols="auto" style="min-width:200px">
        <DateFilter v-model="after" label="Kickoff After" />

      </v-col>
      <v-col cols="auto" style="min-width:200px">
        <DateFilter v-model="before" label="Kickoff Before" />
      </v-col>

    </v-row>

    <!-- Matches Grid -->
    <v-row>
      <v-col
        v-for="match in filteredMatches"
        :key="match.id"
        cols="12"
        md="6"
      >
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>{{ match.home_team }} vs {{ match.away_team }}</span>
            <v-btn icon @click="toggle(match.id)">
              <v-icon>{{ isExpanded(match.id) ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-subtitle>
            {{ match.status }}
          </v-card-subtitle>
          <v-card-text>
            <div class="text-h5">
              {{ match.home_score }} - {{ match.away_score }}
            </div>
          </v-card-text>
          <v-expand-transition>
            <div v-show="isExpanded(match.id)">
              <v-divider class="my-2" />
              <v-list v-if="goalEvents(match).length > 0">
                <v-list-item
                  v-for="(evt, idx) in goalEvents(match)"
                  :key="idx"
                >
                  <v-list-item-title>
                    {{ evt.minute }}' {{ evt.player }} ({{ evt.team }})
                  </v-list-item-title>
                </v-list-item>
              </v-list>
              <v-btn class="mt-2" color="primary" @click="goToMatch(match.id)">
                More Details
              </v-btn>
            </div>
          </v-expand-transition>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import DateFilter from '@/components/DateFilter.vue'

  interface MatchEvent {
    minute: number
    team: string
    player: string
    type: string
  }
  interface Match {
    id: number
    league: string
    home_team: string
    away_team: string
    home_score: number
    away_score: number
    kickoff_time: string
    status: string
    events: MatchEvent[]
  }

  const matches = ref<Match[]>([])
  const expanded = ref<Set<number>>(new Set())
  const league = ref<string | null>(null)
  const after = ref<string | null>(null)
  const before = ref<string | null>(null)
  const router = useRouter()

  const leagues = computed(() =>
    Array.from(new Set(matches.value.map(m => m.league))),
  )

  const filteredMatches = computed(() =>
    matches.value.filter(m => {
      const t = new Date(m.kickoff_time).getTime()

      const leagueOk = league.value ? m.league === league.value : true
      const afterOk = after.value ? t >= new Date(after.value).getTime() : true
      const beforeOk = before.value ? t <= new Date(before.value).getTime() : true

      return leagueOk && afterOk && beforeOk
    }),
  )

  onMounted(async () => {
    const res = await fetch('http://localhost:8000/api/matches')
    matches.value = await res.json()
  })

  function goalEvents (m: Match) {
    return m.events.filter(e => e.type === 'goal')
  }

  function toggle (id: number) {
    if (expanded.value.has(id))
      expanded.value.delete(id)
    else
      expanded.value.add(id)
  }

  function isExpanded (id: number) {
    return expanded.value.has(id)
  }

  function goToMatch (id: number) {
    router.push(`/match/${id}`)
  }
</script>
