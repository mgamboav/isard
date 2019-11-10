
echo "(Re)Building engine protobuffers"
rm -rf ./api/grpc/proto/*.py
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/domain.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/desktops_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/template.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/templates_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/base.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/bases_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/media.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/media_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./api/grpc/proto/engine.proto --python_out=. --grpc_python_out=.
echo "(Re)Building engine protobuffers DONE"
