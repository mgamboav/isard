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

<style lang="scss">
@mixin font($font-family, $font-file) {
  @font-face {
    font-family: $font-family;
    src: url($font-file);
  }
}

@include font('Roboto', './assets/fonts/Roboto-Regular.ttf');
@include font('Roboto Bold', './assets/fonts/Roboto-Bold.ttf');

h1, h2, h3, h4, h5, h6 {
  // Visual
  font-family: 'Roboto Bold', sans-serif;
}

p {
  // Visual
  font-family: 'Roboto', sans-serif;
}
</style>
