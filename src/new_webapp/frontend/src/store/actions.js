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
        commit('updateUsr', payload.usr)
        commit('loginErr', '')
        setCookie('tkn', rsp.getTkn())
        setCookie('usr', payload.usr)
      } else {
        commit('loginErr', err.message)
      }
    })
  },
  logout (context) {
    context.commit('updateTkn', null)
    removeCookie('tkn')
  },
  getDesktops ({ commit, state }) {
    let req = new proto.UserDesktopsGetRequest()
    req.setApi(state.api)
    req.setId(state.usr)

    state.isard.userDesktopsGet(req, { 'tkn': state.tkn }, (err, rsp) => {
      if (err === null) {
        commit('updateDesktops', rsp.getDesktopsList())
        commit('getDesktopsErr', '')
      } else {
        commit('getDesktopsErr', err.message)
      }
    })
  }
}
