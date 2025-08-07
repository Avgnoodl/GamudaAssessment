/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

// Styles
import 'unfonts.css'
import "vuetify/styles"
import '@/styles/override-font.css'

import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'

const app = createApp(App)

// register once, now these tags are available everywhere:
app.component('AppHeader', Header)
app.component('AppSidebar', Sidebar)

registerPlugins(app)
app.mount('#app')
