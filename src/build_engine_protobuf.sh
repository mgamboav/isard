python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/desktops.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/templates.proto --python_out=. --grpc_python_out=.
python3 -m grpc_tools.protoc --proto_path=. ./engine/grpc/proto/engineinfo.proto --python_out=. --grpc_python_out=.
