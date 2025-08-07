<!-- Sidebar.vue -->
<template>
  <v-navigation-drawer
    v-model="drawer"
    :mini-variant="!drawer"
    color="surface"
    elevation="2"
  >
    <v-list nav dense>
      <v-list-item link @click="navigate('home')">
        <v-list-item-icon>
          <v-icon>mdi-home</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Homepage</v-list-item-title>
      </v-list-item>

      <v-list-item link @click="navigate('team-stats')">
        <v-list-item-icon>
          <v-icon>mdi-chart-bar</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Team Stats</v-list-item-title>
      </v-list-item>

      <v-list-item link @click="navigate('league-table')">
        <v-list-item-icon>
          <v-icon>mdi-format-list-numbered</v-icon>
        </v-list-item-icon>
        <v-list-item-title>League Table</v-list-item-title>
      </v-list-item>

      <!-- Help & About Links -->
      <v-divider class="my-2" />
      <v-list-item link @click="navigate('help')">
        <v-list-item-icon>
          <v-icon>mdi-help-circle-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Help</v-list-item-title>
      </v-list-item>
      <v-list-item link @click="navigate('about')">
        <v-list-item-icon>
          <v-icon>mdi-information-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-title>About</v-list-item-title>
      </v-list-item>
    </v-list>

    <!-- Footer or Misc. Section -->
    <v-divider class="my-4" />
    <div class="px-4 text-caption">
      © 2025 Football Tracker
    </div>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

// accept v-model from parent as modelValue
const props = defineProps({
  modelValue: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue'])

// sync internal drawer with parent state
const drawer = computed({
  get: () => props.modelValue,
  set: (val: boolean) => emit('update:modelValue', val)
})

const router = useRouter()
function navigate(name: string) {
  // close drawer then navigate
  emit('update:modelValue', false)
  router.push({ name })
}
</script>

<style scoped>
/* Mini-variant width adjustment */
.v-navigation-drawer--mini-variant {
  width: 56px !important;
}
.v-main__wrap {
  margin-left: 0 !important;
}
</style>