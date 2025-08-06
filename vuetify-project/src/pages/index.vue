<template>
  <v-container>
    <v-row>
      <v-col class="text-h4 mb-4"> Football Match Dashboard</v-col>
    </v-row>
    
    <v-select
      v-model="league"
      class="mb-4"
      clearable
      :items="leagues"
      label="Filter by league"
    />
    <v-row>
      <v-col
        v-for="match in filteredMatches"
        :key="match.id"
        cols="12"
        md="6"
      >
        <v-card>
          <v-card-title>{{ match.home_team }} vs {{ match.away_team }}</v-card-title>
          <v-card-subtitle>{{ formatKickoff(match.kickoff_time) }} — {{ match.status }}</v-card-subtitle>
          <v-card-text>
            <div class="text-h5">{{ match.home_score }} - {{ match.away_score }}</div>
            <v-list v-if="match.events.length > 0">
              <v-list-item
                v-for="(event, index) in match.events"
                :key="index"
              >
                <v-list-item-title>
                  {{ event.minute }}' {{ event.player }} ({{ event.team }})
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'

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
  const league = ref<string | null>(null)

  const leagues = computed(() => Array.from(new Set(matches.value.map(m => m.league))))

  const filteredMatches = computed(() =>
    league.value ? matches.value.filter(m => m.league === league.value) : matches.value,
  )

  onMounted(async () => {
    const res = await fetch('http://localhost:8000/api/matches')
    matches.value = await res.json()
  })

  function formatKickoff (iso: string) {
    return new Date(iso).toLocaleString()
  }
</script>
