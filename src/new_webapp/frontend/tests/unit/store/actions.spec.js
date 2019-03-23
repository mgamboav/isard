import { getCookie, setCookie } from 'tiny-cookie';

import actions from '@/store/actions'
import * as proto from '@/proto/isard_grpc_web_pb'

describe('login', () => {
  let commit
  let state = {
    api: 'v1.0',
    isard: {
      loginLocal: jest.fn().mockImplementationOnce((req, metadata, callback) => {
        callback(null, {
          getTkn: () => 'token'
        })
      }).mockImplementationOnce((req, metadata, callback) => {
        callback({
          message: 'error :('
        }, {})
      })
    },
    loginErr: ''
  }
  let payload

  proto.default = {
    LoginLocalRequest: class {
      setApi() {}
      setUsr() {}
      setPwd() {}
    }
  }

  beforeEach(() => {
    commit = jest.fn()
    payload = {
      usr: 'egoldman',
      pwd: 'P4$$w0rd!'
    }
  })

  it('updates the token with the one that has recieved, removes the possible login errors and adds it to a cookie', () => {
    actions.login({ commit, state }, payload)

    // TODO: Check call parameters
    expect(state.isard.loginLocal).toHaveBeenCalled()
    expect(commit).toHaveBeenCalledWith('updateTkn', 'token')
    expect(commit).toHaveBeenCalledWith('loginErr', '')
    expect(getCookie('tkn')).toBe('token')
  })

  it("updates the login error state if there's an error during the authentication", () => {
    actions.login({ commit, state }, payload)

    // TODO: Check call parameters
    expect(state.isard.loginLocal).toHaveBeenCalled()
    expect(commit).toHaveBeenCalledWith('loginErr', 'error :(')
  })
})

describe('logout', () => {
  it('removes the token from the store and removes the token cookie', () => {
    const context = {
      commit: jest.fn()
    }

    setCookie('tkn', 'token')
    actions.logout(context)

    expect(context.commit).toHaveBeenCalledWith('updateTkn', null)
    expect(getCookie('tkn')).toBe(null)
  })
})
