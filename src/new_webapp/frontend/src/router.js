import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home.vue'
import Login from './views/Login.vue'
import store from './store'

Vue.use(Router)

var router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: {
        showNavBar: false
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path == '/logout') {
    store.dispatch('logout')
    next({
      path: '/login'
    })
  } else if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.tkn === null) {
      next({
        path: '/login'
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
