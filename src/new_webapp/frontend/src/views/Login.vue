<template>
    <b-row id="login" align-h="center">
        <b-col sm="10" md="6" lg="5" xl="4">
            <img src="../assets/logo_black.png" alt="IsardVDI logo (an Isard head icon)" />

            <h1>{{ $t('views.login.title') }}</h1>

            <b-alert id="login-error" variant="danger" :show="loginErr !== ''">{{ loginErr }}</b-alert>

            <b-form @submit="login">
                <b-form-input
                    id="username"
                    type="text"
                    required
                    v-model="form.username"
                    autofocus
                    :placeholder="$t('views.login.form.username')" />

                <b-form-input
                    id="password"
                    type="password"
                    required
                    v-model="form.password"
                    :placeholder="$t('views.login.form.password')" />

                <b-button id="submit" type="submit">{{ $t('views.login.form.login') }}</b-button>
            </b-form>
        </b-col>
    </b-row>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

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
  computed: mapGetters({
    tkn: 'tkn',
    loginErr: 'loginErr'
  }),
  watch: {
    tkn (oldTkn, newTkn) {
      this.redirect()
    }
  },
  methods: {
    login (event) {
      event.preventDefault()

      let payload = {
        'usr': this.form.username,
        'pwd': this.form.password
      }
      this.storeLogin(payload)
    },
    redirect () {
      if (this.tkn !== null) {
        this.$router.push('/')
      }
    },
    ...mapActions({
      storeLogin: 'login'
    })
  },
  mounted: function () {
    this.redirect()
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

    #login-error {
      // Position
      margin-top: 25px;

      // Visual
      text-transform: capitalize;
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
