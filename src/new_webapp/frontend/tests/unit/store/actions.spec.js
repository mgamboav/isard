import { getCookie, setCookie } from 'tiny-cookie'

import actions from '@/store/actions'
import * as proto from '@/proto/isard_grpc_web_pb'

proto.default = {
  LoginLocalRequest: class {
    setApi () {}
    setUsr () {}
    setPwd () {}
  },
  UserDesktopsGetRequest: class {
    setApi () {}
    setId () {}
  }
}

describe('login', () => {
  let commit
  let state = {
    api: 'v1.0',
    isard: {
      loginLocal: jest.fn().mockImplementationOnce((req, metadata, func) => {
        func(null, {
          getTkn: () => 'token'
        })
      }).mockImplementationOnce((req, metadata, func) => {
        func({
          message: 'error :('
        }, {})
      })
    },
    loginErr: ''
  }
  let payload

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

describe('getDesktops', () => {
  let desktops = [{
    'id':          '_nefix_Debian',
    'name':        'Debian',
    'description': 'This is a Debian desktop',
    'status':      'Stopped',
    'detail':      'everything works',
    'user':        'nefix',
    'os':          'linux',
    'options': {
      'viewers': {
        'spice': {
          'fullscreen': true
        }
      }
    }
  }, {
    'id':          '_nefix_NixOS',
    'name':        'NixOS',
    'description': 'This is a NixOS desktop',
    'status':      'Failed',
    'detail':      'no space left in the disk',
    'user':        'nefix',
    'os':          'linux'
  }]

  let commit
  let state = {
    api: 'v1.0',
    isard: {
      userDesktopsGet: jest.fn().mockImplementationOnce((req, metadata, func) => {
        func(null, {
          getDesktopsList: () => desktops
        })
      }).mockImplementationOnce((req, metadata, func) => {
        func({
          message: 'error :('
        }, {})
      })
    },
    user: 'nefix',
    desktops: [],
    getDesktopsErr: ''
  }

  beforeEach(() => {
    commit = jest.fn()
  })

  it('updates the desktops with the ones that has recieved and removes the possible login errors', () => {
    actions.getDesktops({ commit, state })

    // TODO: Check call parameters
    expect(state.isard.userDesktopsGet).toHaveBeenCalled()
    expect(commit).toHaveBeenCalledWith('updateDesktops', desktops)
    expect(commit).toHaveBeenCalledWith('getDesktopsErr', '')
  })

  it("updates the get desktops state if there's an error getting them", () => {
    actions.getDesktops({ commit, state })

    // TODO: Check call parameters
    expect(state.isard.userDesktopsGet).toHaveBeenCalled()
    expect(commit).toHaveBeenCalledWith('getDesktopsErr', 'error :(')
  })
})