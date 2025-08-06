<template>
  <v-container v-if="match">
    <v-row>
      <v-col class="text-h4 mb-2">
        {{ match.home_team }} vs {{ match.away_team }}
      </v-col>
    </v-row>
    <v-row>
      <v-col class="text-h5 mb-4">
        {{ match.home_score }} - {{ match.away_score }}
      </v-col>
    </v-row>
    <v-divider class="my-4">First Half</v-divider>
    <div
      v-for="(evt, idx) in firstHalf"
      :key="idx"
      :class="['d-flex', evt.team === match.home_team ? 'justify-start' : 'justify-end']"
    >
      <div>
        {{ evt.minute }}' {{ evt.player }} - {{ formatType(evt.type) }}
      </div>
    </div>
    <v-divider class="my-4">Second Half</v-divider>
    <div
      v-for="(evt, idx) in secondHalf"
      :key="idx"
      :class="['d-flex', evt.team === match.home_team ? 'justify-start' : 'justify-end']"
    >
      <div>
        {{ evt.minute }}' {{ evt.player }} - {{ formatType(evt.type) }}
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'

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

  const route = useRoute()
  const match = ref<Match | null>(null)

  onMounted(async () => {
    const res = await fetch(`http://localhost:8000/api/matches/${route.params.id}`)
    match.value = await res.json()
  })

  const firstHalf = computed(() =>
    match.value ? match.value.events.filter(e => e.minute <= 45) : [],
  )
  const secondHalf = computed(() =>
    match.value ? match.value.events.filter(e => e.minute > 45) : [],
  )

  function formatType (t: string) {
    switch (t) {
      case 'goal': {
        return 'Goal'
      }
      case 'yellow_card': {
        return 'Yellow Card'
      }
      case 'red_card': {
        return 'Red Card'
      }
      case 'substitution': {
        return 'Substitution'
      }
      default: {
        return t
      }
    }
  }
</script>
