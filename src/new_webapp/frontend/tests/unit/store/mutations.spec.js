import mutations from '@/store/mutations'

describe('updateTkn', () => {
  it('updates the token correctly', () => {
    const state = {
      tkn: null
    }
    mutations.updateTkn(state, 'nogodsnomanagers')
    expect(state.tkn).toBe('nogodsnomanagers')
  })
})

describe('updateUser', () => {
  it('updates the user correctly', () => {
    const state = {
      usr: ''
    }
    mutations.updateUser(state, 'nefix')
    expect(state.usr).toBe('nefix')
  })
})

describe('loginErr', () => {
  it('updates the login error message correctly', () => {
    const state = {
      loginErr: ''
    }
    mutations.loginErr(state, 'incorrect password')
    expect(state.loginErr).toBe('incorrect password')
  })
})

describe('updateDesktops', () => {
  it('updates the domains correctly', () => {
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
      desktops: []
    }
    mutations.updateDesktops(state, d)
    expect(state.desktops).toBe(d)
  })
})

describe('getDesktopsErr', () => {
  it('updates the get desktops error correctly', () => {
    const state = {
      getDesktopsErr: ''
    }
    mutations.getDesktopsErr(state, 'permission denied')
    expect(state.getDesktopsErr).toBe('permission denied')
  })
})