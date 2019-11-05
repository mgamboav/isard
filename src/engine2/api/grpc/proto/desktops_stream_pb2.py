# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/grpc/proto/desktops_stream.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/grpc/proto/desktops_stream.proto',
  package='desktops_stream',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n$api/grpc/proto/desktops_stream.proto\x12\x0f\x64\x65sktops_stream\"\xca\x01\n\x06Viewer\x12\x10\n\x08hostname\x18\x01 \x01(\t\x12\x19\n\x11hostname_external\x18\x02 \x01(\t\x12\x12\n\nport_spice\x18\x05 \x01(\x05\x12\x16\n\x0eport_spice_ssl\x18\x06 \x01(\x05\x12\x10\n\x08port_vnc\x18\x07 \x01(\x05\x12\x1a\n\x12port_vnc_websocket\x18\x08 \x01(\x05\x12\x0e\n\x06passwd\x18\t \x01(\t\x12\x13\n\x0b\x63lient_addr\x18\n \x01(\t\x12\x14\n\x0c\x63lient_since\x18\x0b \x01(\x02\"\x17\n\x15\x44\x65sktopsStreamRequest\"\x97\x02\n\x16\x44\x65sktopsStreamResponse\x12\x12\n\ndesktop_id\x18\x01 \x01(\t\x12<\n\x05state\x18\x02 \x01(\x0e\x32-.desktops_stream.DesktopsStreamResponse.State\x12\x0e\n\x06\x64\x65tail\x18\x03 \x01(\t\x12\x14\n\x0cnext_actions\x18\x04 \x03(\t\x12\'\n\x06viewer\x18\x05 \x01(\x0b\x32\x17.desktops_stream.Viewer\"\\\n\x05State\x12\x0b\n\x07STOPPED\x10\x00\x12\x0b\n\x07STARTED\x10\x01\x12\n\n\x06PAUSED\x10\x02\x12\x0b\n\x07\x44\x45LETED\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04\x12\x0b\n\x07UNKNOWN\x10\x05\x12\x07\n\x03NEW\x10\x06\x32p\n\x0e\x44\x65sktopsStream\x12^\n\x07\x43hanges\x12&.desktops_stream.DesktopsStreamRequest\x1a\'.desktops_stream.DesktopsStreamResponse\"\x00\x30\x01\x62\x06proto3')
)



_DESKTOPSSTREAMRESPONSE_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='desktops_stream.DesktopsStreamResponse.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STOPPED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STARTED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAUSED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DELETED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEW', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=475,
  serialized_end=567,
)
_sym_db.RegisterEnumDescriptor(_DESKTOPSSTREAMRESPONSE_STATE)


_VIEWER = _descriptor.Descriptor(
  name='Viewer',
  full_name='desktops_stream.Viewer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hostname', full_name='desktops_stream.Viewer.hostname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hostname_external', full_name='desktops_stream.Viewer.hostname_external', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port_spice', full_name='desktops_stream.Viewer.port_spice', index=2,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port_spice_ssl', full_name='desktops_stream.Viewer.port_spice_ssl', index=3,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port_vnc', full_name='desktops_stream.Viewer.port_vnc', index=4,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port_vnc_websocket', full_name='desktops_stream.Viewer.port_vnc_websocket', index=5,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='passwd', full_name='desktops_stream.Viewer.passwd', index=6,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_addr', full_name='desktops_stream.Viewer.client_addr', index=7,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_since', full_name='desktops_stream.Viewer.client_since', index=8,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=58,
  serialized_end=260,
)


_DESKTOPSSTREAMREQUEST = _descriptor.Descriptor(
  name='DesktopsStreamRequest',
  full_name='desktops_stream.DesktopsStreamRequest',
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
  serialized_start=262,
  serialized_end=285,
)


_DESKTOPSSTREAMRESPONSE = _descriptor.Descriptor(
  name='DesktopsStreamResponse',
  full_name='desktops_stream.DesktopsStreamResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='desktop_id', full_name='desktops_stream.DesktopsStreamResponse.desktop_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='desktops_stream.DesktopsStreamResponse.state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='detail', full_name='desktops_stream.DesktopsStreamResponse.detail', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_actions', full_name='desktops_stream.DesktopsStreamResponse.next_actions', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='viewer', full_name='desktops_stream.DesktopsStreamResponse.viewer', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DESKTOPSSTREAMRESPONSE_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=288,
  serialized_end=567,
)

_DESKTOPSSTREAMRESPONSE.fields_by_name['state'].enum_type = _DESKTOPSSTREAMRESPONSE_STATE
_DESKTOPSSTREAMRESPONSE.fields_by_name['viewer'].message_type = _VIEWER
_DESKTOPSSTREAMRESPONSE_STATE.containing_type = _DESKTOPSSTREAMRESPONSE
DESCRIPTOR.message_types_by_name['Viewer'] = _VIEWER
DESCRIPTOR.message_types_by_name['DesktopsStreamRequest'] = _DESKTOPSSTREAMREQUEST
DESCRIPTOR.message_types_by_name['DesktopsStreamResponse'] = _DESKTOPSSTREAMRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Viewer = _reflection.GeneratedProtocolMessageType('Viewer', (_message.Message,), {
  'DESCRIPTOR' : _VIEWER,
  '__module__' : 'api.grpc.proto.desktops_stream_pb2'
  # @@protoc_insertion_point(class_scope:desktops_stream.Viewer)
  })
_sym_db.RegisterMessage(Viewer)

DesktopsStreamRequest = _reflection.GeneratedProtocolMessageType('DesktopsStreamRequest', (_message.Message,), {
  'DESCRIPTOR' : _DESKTOPSSTREAMREQUEST,
  '__module__' : 'api.grpc.proto.desktops_stream_pb2'
  # @@protoc_insertion_point(class_scope:desktops_stream.DesktopsStreamRequest)
  })
_sym_db.RegisterMessage(DesktopsStreamRequest)

DesktopsStreamResponse = _reflection.GeneratedProtocolMessageType('DesktopsStreamResponse', (_message.Message,), {
  'DESCRIPTOR' : _DESKTOPSSTREAMRESPONSE,
  '__module__' : 'api.grpc.proto.desktops_stream_pb2'
  # @@protoc_insertion_point(class_scope:desktops_stream.DesktopsStreamResponse)
  })
_sym_db.RegisterMessage(DesktopsStreamResponse)



_DESKTOPSSTREAM = _descriptor.ServiceDescriptor(
  name='DesktopsStream',
  full_name='desktops_stream.DesktopsStream',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=569,
  serialized_end=681,
  methods=[
  _descriptor.MethodDescriptor(
    name='Changes',
    full_name='desktops_stream.DesktopsStream.Changes',
    index=0,
    containing_service=None,
    input_type=_DESKTOPSSTREAMREQUEST,
    output_type=_DESKTOPSSTREAMRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DESKTOPSSTREAM)

DESCRIPTOR.services_by_name['DesktopsStream'] = _DESKTOPSSTREAM

# @@protoc_insertion_point(module_scope)
