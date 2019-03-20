import Vue from 'vue'
import Vuex from 'vuex'
import { get as getCookie, set as setCookie } from 'tiny-cookie'

import proto from './proto/isard_grpc_web_pb'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    api: 'v1.0',
    isard: new proto.IsardClient('http://localhost:1024', null, null),
    tkn: getCookie('tkn')
  },
  getters: {
    tkn: state => state.tkn
  },
  mutations: {
    updateTkn (state, tkn) {
      state.tkn = tkn
    }
  },
  actions: {
    login ({ commit, state }, payload) {
      let req = new proto.LoginLocalRequest()
      req.setApi(this.api)
      req.setUsr(payload.usr)
      req.setPwd(payload.pwd)

      state.isard.loginLocal(req, {}, (err, rsp) => {
        if (err === null) {
          commit('updateTkn', rsp.getTkn())
          setCookie('tkn', rsp.getTkn())
        } else {
          // TODO: Manage error!
          console.log(err)
        }
      })
    }
  }
})
