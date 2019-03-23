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

describe('loginErr', () => {
  it('updates the login error message correctly', () => {
    const state = {
      loginErr: ''
    }
    mutations.loginErr(state, 'incorrect password')
    expect(state.loginErr).toBe('incorrect password')
  })
})