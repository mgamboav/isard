# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from api.grpc.proto import media_stream_pb2 as api_dot_grpc_dot_proto_dot_media__stream__pb2


class MediaStreamStub(object):
  """import "google/protobuf/empty.proto"; 
  import "google/protobuf/any.proto";

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Changes = channel.unary_stream(
        '/templates_stream.MediaStream/Changes',
        request_serializer=api_dot_grpc_dot_proto_dot_media__stream__pb2.MediaStreamRequest.SerializeToString,
        response_deserializer=api_dot_grpc_dot_proto_dot_media__stream__pb2.MediaStreamResponse.FromString,
        )


class MediaStreamServicer(object):
  """import "google/protobuf/empty.proto"; 
  import "google/protobuf/any.proto";

  """

  def Changes(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MediaStreamServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Changes': grpc.unary_stream_rpc_method_handler(
          servicer.Changes,
          request_deserializer=api_dot_grpc_dot_proto_dot_media__stream__pb2.MediaStreamRequest.FromString,
          response_serializer=api_dot_grpc_dot_proto_dot_media__stream__pb2.MediaStreamResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'templates_stream.MediaStream', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
