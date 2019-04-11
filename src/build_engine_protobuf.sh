rm -rf ./engine/grpc/proto/__pycache__
rm ./engine/grpc/proto/*.py
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/desktop.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/desktops_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/template.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/templates_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/media.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/media_stream.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/engine.proto --python_out=. --grpc_python_out=.

