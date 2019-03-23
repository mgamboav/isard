import { setCookie, removeCookie } from 'tiny-cookie'

import proto from '@/proto/isard_grpc_web_pb'

export default {
  login ({ commit, state }, payload) {
    let req = new proto.LoginLocalRequest()
    req.setApi(state.api)
    req.setUsr(payload.usr)
    req.setPwd(payload.pwd)

    state.isard.loginLocal(req, {}, (err, rsp) => {
      if (err === null) {
        commit('updateTkn', rsp.getTkn())
        commit('loginErr', '')
        setCookie('tkn', rsp.getTkn())
      } else {
        commit('loginErr', err.message)
      }
    })
  },
  logout (context) {
    context.commit('updateTkn', null)
    removeCookie('tkn')
  }
}
