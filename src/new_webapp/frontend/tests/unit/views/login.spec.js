import { createLocalVue, mount, shallowMount } from '@vue/test-utils'

import Vuex from 'vuex'
import Router from 'vue-router'
import i18n from '@/i18n'

import BootstrapVue from 'bootstrap-vue'

import Login from '@/views/Login.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
localVue.use(Router)

localVue.use(BootstrapVue)

const router = new Router()

describe('Login.vue', () => {
  let state
  let getters
  let mutations
  let actions
  let store

  beforeEach(() => {
    state = {
      tkn: null,
      loginErr: ''
    }
    getters = {
      tkn: state => state.tkn,
      loginErr: state => state.loginErr
    }
    mutations = {
      setTkn: (state, tkn) => {
        state.tkn = tkn
      }
    }
    actions = {
      login: jest.fn(),
      setTkn ({ commit }, tkn) {
        commit('setTkn', tkn)
      }
    }

    store = new Vuex.Store({
      state,
      getters,
      mutations,
      actions
    })
  })

  it('dispatches "login" when the form is submitted', () => {
    const wrapper = mount(Login, {
      store,
      localVue,
      i18n
    })

    // The login error alert shouldn't be visible
    expect(wrapper.find('#login-error').exists()).toBe(false)

    wrapper.find('#username').setValue = 'username'
    wrapper.find('#password').setValue = 'P4$$w0rd!'
    wrapper.find('form').trigger('submit')

    expect(actions.login).toHaveBeenCalled()
  })

  it("redirects to the root of the app if there's a token", () => {
    state.tkn = 'token!'

    const wrapper = shallowMount(Login, {
      store,
      localVue,
      router,
      i18n
    })

    expect(wrapper.vm.$route.path).toBe('/')
  })

  it('redirects to the root of the app after a successful login', () => {
    const wrapper = shallowMount(Login, {
      store,
      localVue,
      router,
      i18n
    })

    wrapper.vm.$router.push('/login')
    expect(wrapper.vm.$route.path).toBe('/login')

    wrapper.vm.$store.dispatch('setTkn', 'token!')
    expect(wrapper.vm.$route.path).toBe('/')
  })

  it("the login error alert is shown when there's a login error", () => {
    state.loginErr = 'authentication error'

    const wrapper = mount(Login, {
      store,
      localVue,
      i18n
    })

    const alert = wrapper.find('#login-error')
    expect(alert.name()).toBe('BAlert')
    expect(alert.text()).toBe('authentication error')
  })
})
