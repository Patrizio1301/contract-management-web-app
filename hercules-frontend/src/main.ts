import './assets/main.css'

// Quasar globally
import '@quasar/extras/material-icons/material-icons.css'
// Import Quasar css
import 'quasar/src/css/index.sass'


import { createApp } from 'vue'
import { createPinia } from 'pinia'
import {Quasar} from 'quasar'

import { VueFire, VueFireAuth } from 'vuefire'

import { initializeApp } from 'firebase/app'
import { getFirestore, collection } from 'firebase/firestore'
// ... other firebase imports


const firebaseApp = initializeApp({});



// used for the firestore refs
const db = getFirestore(firebaseApp)

// here we can export reusable database references
export const todosRef = collection(db, 'todos')



import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
})

app.use(VueFire, {
  // imported above but could also just be created here
  firebaseApp,
  modules: [
    // we will see other modules later on
    VueFireAuth(),
  ],
})

app.mount('#app')
