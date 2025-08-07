<template>
  <v-container v-if="match">
    <!-- Hero / Match header -->
    <v-sheet
      class="d-flex flex-column align-center justify-center mb-6 match-hero"
      elevation="1"
      height="200"
    >
      <div class="text-h4 font-weight-bold">
        {{ match.home_team }} vs {{ match.away_team }}
      </div>
      <div class="text-h2 font-weight-bold">
        {{ match.home_score }} - {{ match.away_score }}
      </div>
    </v-sheet>

    <!-- Events Card -->
    <v-sheet elevation="2" class="pa-4 match-events">
      <!-- First Half -->
      <v-divider class="my-4">First Half</v-divider>
      <div
        v-for="(evt, idx) in firstHalf"
        :key="idx"
        :class="['d-flex mb-2', evt.team === match.home_team ? 'justify-start' : 'justify-end']"
      >
        <div class="d-flex align-center">
          <!-- Home side layout -->
          <template v-if="evt.team === match.home_team">
            <span class="mr-1">{{ evt.minute }}'</span>
            <span class="mr-1">
              <template v-if="evt.type === 'substitution'">
                {{ evt.sub_in }} in for {{ evt.player }}
              </template>
              <template v-else>
                {{ evt.player }}
              </template>
            </span>
            <span class="mr-1">{{ iconForType(evt.type) }}</span>
            <span class="subtitle-2">{{ formatType(evt.type) }}</span>
          </template>

          <!-- Away side layout -->
          <template v-else>
            <span class="subtitle-2 mr-1">{{ formatType(evt.type) }}</span>
            <span class="mr-1">{{ iconForType(evt.type) }}</span>
            <span class="mr-1">
              <template v-if="evt.type === 'substitution'">
                {{ evt.sub_in }} in for {{ evt.player }}
              </template>
              <template v-else>
                {{ evt.player }}
              </template>
            </span>
            <span>{{ evt.minute }}'</span>
          </template>
        </div>
      </div>

      <!-- Second Half -->
      <v-divider class="my-4">Second Half</v-divider>
      <div
        v-for="(evt, idx) in secondHalf"
        :key="idx"
        :class="['d-flex mb-2', evt.team === match.home_team ? 'justify-start' : 'justify-end']"
      >
        <div class="d-flex align-center">
          <template v-if="evt.team === match.home_team">
            <span class="mr-1">{{ evt.minute }}'</span>
            <span class="mr-1">
              <template v-if="evt.type === 'substitution'">
                {{ evt.sub_in }} in for {{ evt.player }}
              </template>
              <template v-else>
                {{ evt.player }}
              </template>
            </span>
            <span class="mr-1">{{ iconForType(evt.type) }}</span>
            <span class="subtitle-2">{{ formatType(evt.type) }}</span>
          </template>
          <template v-else>
            <span class="subtitle-2 mr-1">{{ formatType(evt.type) }}</span>
            <span class="mr-1">{{ iconForType(evt.type) }}</span>
            <span class="mr-1">
              <template v-if="evt.type === 'substitution'">
                {{ evt.sub_in }} in for {{ evt.player }}
              </template>
              <template v-else>
                {{ evt.player }}
              </template>
            </span>
            <span>{{ evt.minute }}'</span>
          </template>
        </div>
      </div>
    </v-sheet>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

interface MatchEvent {
  minute: number
  team: string
  player: string      // player going off (or performing the action)
  type: string
  sub_in?: string     // player coming on (only for substitutions)
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
  match.value ? match.value.events.filter(e => e.minute <= 45) : []
)
const secondHalf = computed(() =>
  match.value ? match.value.events.filter(e => e.minute > 45) : []
)

function formatType(t: string) {
  switch (t) {
    case 'goal':           return 'Goal'
    case 'penalty_goal':   return 'Penalty Goal'
    case 'yellow_card':    return 'Yellow Card'
    case 'red_card':       return 'Red Card'
    case 'substitution':   return 'Substitution'
    default:               return t.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
  }
}

function iconForType(t: string) {
  switch (t) {
    case 'goal':           return '⚽'
    case 'penalty_goal':   return '⚽'
    case 'own_goal':       return '😵‍💫'
    case 'yellow_card':    return '🟨'
    case 'red_card':       return '🟥'
    case 'corner':         return '↪️'
    case 'throw_in':       return '↩️'
    case 'goal_kick':      return '🥅'
    case 'free_kick':      return '➕'
    case 'offside':        return '🚫'
    case 'handball':       return '✋'
    case 'foul':           return '👢'
    case 'penalty_missed': return '❌'
    case 'penalty_saved':  return '🧤'
    case 'injury':         return '⛑️'
    case 'substitution':   return '🔄'
    case 'var_check':      return '📺'
    case 'var':            return '🔍'
    case 'var_overturned': return '🔄'
    default:               return '❔'
  }
}
</script>
