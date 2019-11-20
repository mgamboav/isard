from protobuf_gen import remap, wrap

# all of the _pb2 modules will now be importable through `etcd3py.pb_mods.*`
# for example a module "google/api/http.proto" will be available as "etcd3py.pb_mods.google.api.http_pb2"
remap(
    # the working directory is given as the parent directory of the package folder (etcd3py in this case).
    '.',
    'etcd3py.pb_mods',
    # .proto include directories
    [
        './pb-includes/grpc-gateway/third_party/googleapis',
        './pb-includes/etcd',
        './pb-includes/protobuf',
    ],
    # .proto files to be included in the distribution
    [
        './api/grpc/proto/domain_enums.proto',
        './api/grpc/proto/domain.proto',
    ]
)
