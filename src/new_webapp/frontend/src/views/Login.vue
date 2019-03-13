<template>
    <b-row id="login" align-h="center">
        <b-col sm="10" md="6" lg="5" xl="4">
            <img src="../assets/logo_black.png" alt="IsardVDI logo (an Isard head icon)" />

            <h1>IsardVDI Login</h1>

            <b-form @submit="login">
                <b-form-input
                    id="username"
                    type="text"
                    required
                    v-model="form.username"
                    autofocus
                    placeholder="Username" />

                <b-form-input
                    id="password"
                    type="password"
                    required
                    v-model="form.password"
                    placeholder="Password" />

                <b-button type="submit">Login</b-button>
            </b-form>
        </b-col>
    </b-row>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    login (event) {
      event.preventDefault()
      console.log('Logged in!')
    }
  }
}
</script>

<style lang="scss" scoped>
#login {
    // Position
    margin-top: 100px;
    text-align: center;

    img {
        // Size
        height: 150px;

        // Position
        margin-bottom: 25px;
    }

    form {
        // Position
        margin: 25px;

        input {
            // Position
            margin-bottom: 18px;
        }
    }
}
</style>
