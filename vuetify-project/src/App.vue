<template>
  <v-app>
<AppHeader @toggle-sidebar="drawer = !drawer" />
<!-- bind with default v-model -->
<AppSidebar v-model="drawer" />
    <v-main>
    <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
const drawer = ref(false)
  //
</script>
