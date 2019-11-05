# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/grpc/proto/base.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/grpc/proto/base.proto',
  package='base',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x19\x61pi/grpc/proto/base.proto\x12\x04\x62\x61se\x1a\x19google/protobuf/any.proto\"\x1d\n\nGetRequest\x12\x0f\n\x07\x62\x61se_id\x18\x01 \x01(\t\"1\n\x0bGetResponse\x12\"\n\x04\x62\x61se\x18\x01 \x03(\x0b\x32\x14.google.protobuf.Any\"\r\n\x0bListRequest\"\x1d\n\x0cListResponse\x12\r\n\x05\x62\x61ses\x18\x01 \x03(\t2e\n\x04\x42\x61se\x12,\n\x03Get\x12\x10.base.GetRequest\x1a\x11.base.GetResponse\"\x00\x12/\n\x04List\x12\x11.base.ListRequest\x1a\x12.base.ListResponse\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,])




_GETREQUEST = _descriptor.Descriptor(
  name='GetRequest',
  full_name='base.GetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_id', full_name='base.GetRequest.base_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=91,
)


_GETRESPONSE = _descriptor.Descriptor(
  name='GetResponse',
  full_name='base.GetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base', full_name='base.GetResponse.base', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=93,
  serialized_end=142,
)


_LISTREQUEST = _descriptor.Descriptor(
  name='ListRequest',
  full_name='base.ListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=157,
)


_LISTRESPONSE = _descriptor.Descriptor(
  name='ListResponse',
  full_name='base.ListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bases', full_name='base.ListResponse.bases', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=188,
)

_GETRESPONSE.fields_by_name['base'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['GetRequest'] = _GETREQUEST
DESCRIPTOR.message_types_by_name['GetResponse'] = _GETRESPONSE
DESCRIPTOR.message_types_by_name['ListRequest'] = _LISTREQUEST
DESCRIPTOR.message_types_by_name['ListResponse'] = _LISTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETREQUEST,
  '__module__' : 'api.grpc.proto.base_pb2'
  # @@protoc_insertion_point(class_scope:base.GetRequest)
  })
_sym_db.RegisterMessage(GetRequest)

GetResponse = _reflection.GeneratedProtocolMessageType('GetResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETRESPONSE,
  '__module__' : 'api.grpc.proto.base_pb2'
  # @@protoc_insertion_point(class_scope:base.GetResponse)
  })
_sym_db.RegisterMessage(GetResponse)

ListRequest = _reflection.GeneratedProtocolMessageType('ListRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTREQUEST,
  '__module__' : 'api.grpc.proto.base_pb2'
  # @@protoc_insertion_point(class_scope:base.ListRequest)
  })
_sym_db.RegisterMessage(ListRequest)

ListResponse = _reflection.GeneratedProtocolMessageType('ListResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTRESPONSE,
  '__module__' : 'api.grpc.proto.base_pb2'
  # @@protoc_insertion_point(class_scope:base.ListResponse)
  })
_sym_db.RegisterMessage(ListResponse)



_BASE = _descriptor.ServiceDescriptor(
  name='Base',
  full_name='base.Base',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=190,
  serialized_end=291,
  methods=[
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='base.Base.Get',
    index=0,
    containing_service=None,
    input_type=_GETREQUEST,
    output_type=_GETRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='List',
    full_name='base.Base.List',
    index=1,
    containing_service=None,
    input_type=_LISTREQUEST,
    output_type=_LISTRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_BASE)

DESCRIPTOR.services_by_name['Base'] = _BASE

# @@protoc_insertion_point(module_scope)
