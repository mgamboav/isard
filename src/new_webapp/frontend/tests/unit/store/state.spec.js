import state from '@/store/state'

describe('state.js', () => {
  it('initializes the state correctly', () => {
    expect(state.api).toBe('v1.0')
    expect(state.isard).toEqual({
      'client_': {
        'format_': 'text',
        'suppressCorsPreflight_': false
      },
      'credentials_': null,
      'hostname_': 'http://localhost:1024',
      'options_': {
        'format': 'text'
      }
    })
    expect(state.tkn).toBe(null)
    expect(state.usr).toBe('')
    expect(state.loginErr).toBe('')
    expect(state.desktops).toEqual([])
    expect(state.getDesktopsErr).toBe('')
  })
})
