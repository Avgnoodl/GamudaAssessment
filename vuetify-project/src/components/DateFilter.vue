<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    offset-y
    transition="scale-transition"
    min-width="auto"
  >
    <!-- Activator: a read-only text field showing formatted date -->
    <template #activator="{ props }">
      <v-text-field
        v-bind="props"
        v-model="displayValue"
        readonly
        clearable
        :label="label"
        prepend-inner-icon="mdi-calendar-clock"
        style="max-width: 200px"
        @click:clear="clearDate"
      />
    </template>

    <!-- Date picker: raw ISO strings or Date objects -->
    <v-date-picker
      v-model="pickerValue"
      @update:model-value="onPickerChange"
      :show-current="true"
      scrollable
    />
  </v-menu>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'

const props = defineProps<{ modelValue: string | null; label?: string }>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void
}>()

// pickerValue holds the raw value from the date-picker
const pickerValue = ref<string | Date | null>(props.modelValue)
// displayValue shows the formatted date string
const displayValue = ref<string | null>(null)
// controls menu open/close
const menu = ref(false)

// helper to format "Wed, Aug 6 2025"
function formatDisplayDate(d: Date): string {
  const wd = d.toLocaleDateString('en-US', { weekday: 'short' })
  const mon = d.toLocaleDateString('en-US', { month: 'short' })
  const day = d.getDate()
  const yr = d.getFullYear()
  return `${wd}, ${mon} ${day} ${yr}`
}

// Sync props.modelValue into internal state
watch(
  () => props.modelValue,
  (val) => {
    pickerValue.value = val
    if (val) {
      const d = new Date(val)
      displayValue.value = formatDisplayDate(d)
    } else {
      displayValue.value = null
    }
  },
  { immediate: true }
)

// Normalize picker output, emit formatted date, close menu
function onPickerChange(val: string | Date | null) {
  if (val) {
    const d = typeof val === 'string' ? new Date(val) : val
    const isoDate = d.toISOString().slice(0, 10)
    displayValue.value = formatDisplayDate(d)
    emit('update:modelValue', isoDate)
  } else {
    displayValue.value = null
    emit('update:modelValue', null)
  }
  menu.value = false
}

// Handle clear icon click
function clearDate() {
  displayValue.value = null
  pickerValue.value = null
  emit('update:modelValue', null)
  // leave menu closed
}
</script>
