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
