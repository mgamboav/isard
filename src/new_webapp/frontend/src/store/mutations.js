export default {
  updateTkn (state, tkn) {
    state.tkn = tkn
  },
  updateUser (state, usr) {
    state.usr = usr
  },
  loginErr (state, err) {
    state.loginErr = err
  },
  updateDesktops (state, desktops) {
    state.desktops = desktops
  },
  getDesktopsErr (state, err) {
    state.getDesktopsErr = err
  }
}
