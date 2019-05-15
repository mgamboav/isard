<template>
  <div class="home">
    <b-alert
      id="get-desktops-error"
      variant="danger"
      :show="getDesktopsErr !== ''"
    >{{ getDesktopsErr }}</b-alert>

    <div class="desktops">
      <simple-desktop v-for="desktop in desktops" :key="desktop.id" :desktop="desktop"/>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import SimpleDesktop from '@/components/SimpleDesktop.vue'

export default {
  name: 'home',
  components: {
    SimpleDesktop
  },
  computed: {
    ...mapGetters(['desktops', 'getDesktopsErr'])
  },
  mounted() {
    this.$store.dispatch('getDesktops')
  }
}
</script>

<style lang="scss" scoped>
.desktops {
  display: flex;
  flex-flow: row wrap;

  .simple-desktop {
    width: 300px;
    margin: 18px;
  }
}
</style>
