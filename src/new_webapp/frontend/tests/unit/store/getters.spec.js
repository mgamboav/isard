import getters from '@/store/getters'

describe('tkn', () => {
  it('returns the value of the state', () => {
    const state = {
      tkn: 'token'
    }
    expect(getters.tkn(state)).toBe('token')
  })
})

describe('loginErr', () => {
  it('returns the value of the state', () => {
    const state = {
      loginErr: 'authentication error: incorrect password'
    }

    expect(getters.loginErr(state)).toBe('authentication error: incorrect password')
  })
})

describe('desktops', () => {
  it('returns the value of the state', () => {
    const d = [{
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
    const state = {
      desktops: d
    }

    expect(getters.desktops(state)).toBe(d)
  })
})

describe('getDesktopsErr', () => {
  it('returns the value fo the state', () => {
    const state = {
      getDesktopsErr: 'permission denied'
    }

    expect(getters.getDesktopsErr(state)).toBe('permission denied')
  })
})
