<!-- Header.vue -->
<template>
  <v-app-bar app class="header" dark>
    <!-- Toggle Sidebar -->
    <v-btn icon @click="$emit('toggle-sidebar')">
      <v-icon>mdi-menu</v-icon>
    </v-btn>

    <!-- Logo and Title as Router Link -->
    <router-link to="/" class="d-flex align-center text-decoration-none" style="color: inherit;">
      <v-img
        src="@/assets/Football_Logo.png"
        alt="Logo"
        contain
        max-width="40"
        class="mx-2"
      />
      <v-toolbar-title class="text-white" style="width: 300px;">Football Match Tracker</v-toolbar-title>
    </router-link>

    <v-spacer />
  </v-app-bar>
</template>
<script setup lang="ts">

</script>

<style scoped>
</style>