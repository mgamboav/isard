import proto from '@/proto/isard_grpc_web_pb'

import { getCookie } from 'tiny-cookie'

export default {
  api: 'v1.0',
  isard: new proto.IsardClient(window.location.hostname + '/backend', null, null),
  tkn: getCookie('tkn'),
  usr: getCookie('usr'),
  loginErr: '',
  desktops: [],
  getDesktopsErr: ''
}
