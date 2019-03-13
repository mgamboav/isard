<template>
  <div id="app">
    <div id="nav" v-show="showNavBar()">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <b-container>
      <router-view/>
    </b-container>
  </div>
</template>

<script>
export default {
  methods: {
    showNavBar: function () {
      if (this.$route.meta.showNavBar === false) {
        return false
      }

      return true
    }
  }
}
</script>
