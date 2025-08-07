<template>
  <!-- Hero / Landing intro (full-width) -->
  <v-sheet class="d-flex flex-column justify-center hero pt-2 pb-10" elevation="0" height="160">
    <div class="w-100 text-center">
      <h1 class="display-2 font-weight-bold mb-2">
        Football Match Tracker
      </h1>
    </div>
    <div class="w-100 text-center">
      <p class="subtitle-1">
        Track live scores, upcoming fixtures and past results all in one sleek dashboard.
        Filter by league or kickoff time, then click any match for goal highlights and more.
      </p>
    </div>
  </v-sheet>

  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <!-- Filters Row -->

        <v-row justify="end">
          <v-spacer />
          <v-select
            v-model="league"
            class="ma-3"
            clearable
            :items="leagues"
            label="Filter by league"
            style="max-width:250px"
          />
          <v-col cols="auto" style="min-width:300px">
            <DateFilter v-model="before" label="Kickoff Before" />
          </v-col>
          <v-col cols="auto" style="min-width:300px">
            <DateFilter v-model="after" label="Kickoff After" />
          </v-col>

        </v-row>

        <!-- 3) Grouped match lists with dividers -->
        <div v-for="(group, label) in filteredByStatus" :key="label">
          <v-divider class="my-4" />
          <div class="text-h6 mb-2 text-capitalize">{{ label }} matches</div>
          <v-row>
            <!-- if no matches in this group… -->
            <template v-if="group.length === 0">
              <v-col cols="12">
                <div class="subtitle-1 text-center">
                  No {{ label }} matches
                </div>
              </v-col>
            </template>

            <!-- otherwise render the cards -->
            <template v-else>
              <v-col v-for="match in group" :key="match.id" cols="12" md="6">
                <v-card class="match-card">
                  <v-card-title class="d-flex justify-space-between align-center">
                    <span>{{ match.home_team }} vs {{ match.away_team }}</span>
                    <v-btn flat icon @click="toggle(match.id)">
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

                    <v-sheet v-show="isExpanded(match.id)" class="pa-0" color="transparent" elevation="0">
                      <v-divider class="my-2" />
                      <v-list v-if="highlightEvents(match).length > 0">
                        <v-list-item v-for="(evt, i) in highlightEvents(match)" :key="i">
                          <v-list-item-title>
                            {{ evt.minute }}' {{ evt.player }}
                            <template v-if="evt.type === 'substitution'">
                              → {{ evt.sub_in }}
                            </template>
                            ({{ evt.team }}) - {{ evt.type }}
                          </v-list-item-title>
                        </v-list-item>
                      </v-list>

                      <v-btn class="detail-button ma-4" @click="goToMatch(match.id)">
                        More Details
                      </v-btn>
                    </v-sheet>
                  </v-expand-transition>
                </v-card>
              </v-col>
            </template>
          </v-row>
        </div>

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
  import { storeToRefs } from 'pinia'
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import DateFilter from '@/components/DateFilter.vue'
  import { type Match, useMatches } from '@/stores/matches'

  const matchesStore = useMatches()
  const { matches } = storeToRefs(matchesStore)
  const expanded = ref<Set<number>>(new Set())
  const league = ref<string | null>(null)
  const after = ref<string | null>(null)
  const before = ref<string | null>(null)
  const router = useRouter()

  const leagues = computed(() =>
    Array.from(new Set(matches.value.map(m => m.league))),
  )

  const filtered = computed(() =>
    matches.value.filter(m => {
      const t = new Date(m.kickoff_time).getTime()
      return (
        (!league.value || m.league === league.value)
        && (!after.value || t >= new Date(after.value).getTime())
        && (!before.value || t <= new Date(before.value).getTime())
      )
    }),
  )

  // 3) split into status groups
  const filteredByStatus = computed(() => {
    const groups: Record<string, Match[]> = {
      live: [], scheduled: [], finished: [],
    }
    for (const m of filtered.value) {
      if (groups[m.status]) groups[m.status].push(m)
      else groups.scheduled.push(m)
    }
    return groups
  })

  onMounted(() => {
    matchesStore.connectWS()
  })
  function highlightEvents (m: Match) {
    return m.events.filter(e => ['goal', 'yellow_card', 'substitution'].includes(e.type))
  }
  function toggle (id: number) {
    expanded.value.has(id)
      ? expanded.value.delete(id)
      : expanded.value.add(id)
  }
  function isExpanded (id: number) {
    return expanded.value.has(id)
  }
  function goToMatch (id: number) {
    router.push(`/match/${id}`)
  }
</script>

<style scoped></style>
