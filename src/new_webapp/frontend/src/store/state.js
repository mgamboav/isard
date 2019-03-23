import proto from '@/proto/isard_grpc_web_pb'

import { getCookie } from 'tiny-cookie'

export default {
  api: 'v1.0',
  isard: new proto.IsardClient('http://localhost:1024', null, null),
  tkn: getCookie('tkn'),
  loginErr: ''
}
