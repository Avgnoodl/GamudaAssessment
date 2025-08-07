<!-- Header.vue -->
<template>
  <v-app-bar app color="primary" dark>
    <!-- Toggle Sidebar -->
    <v-btn icon @click="$emit('toggle-sidebar')">
      <v-icon>mdi-menu</v-icon>
    </v-btn>

    <!-- Page Logo -->
    <v-img
      src="@/assets/logo.png"
      alt="Logo"
      contain
      max-width="40"
      class="mx-2"
    />

    <!-- Page Title -->
    <v-toolbar-title>Football Match Tracker</v-toolbar-title>

    <v-spacer />

    <!-- Optional Action Icons -->
    <v-btn icon>
      <v-icon>mdi-bell-outline</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-account-circle</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
// Emits 'toggle-sidebar' event to parent

</script>

<style scoped>
/* Customize app-bar height or padding if needed */
</style>