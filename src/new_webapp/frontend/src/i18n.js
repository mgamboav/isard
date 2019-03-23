import Vue from 'vue'
import VueI18n from 'vue-i18n'

import en from '@/lang/en'
import ca from '@/lang/ca'

Vue.use(VueI18n)

export default new VueI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    ca
  }
})
