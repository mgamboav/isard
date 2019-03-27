#!/bin/sh

protoc -I . \
  -I $GOPATH/src \
  -I proto/third_party \
  --grpc-gateway_out=logtostderr=true:. \
  --go_out=plugins=grpc:. \
  --swagger_out=logtostderr=true:. \
  proto/isard.proto

cd ../frontend
rm -rf proto
cp -R ../backend/proto .

find proto/third_party -type f | while IFS= read -r -d $'\n' f; do
  protoc -I . \
    -I proto/third_party \
    --js_out=import_style=commonjs:. \
    --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. \
    "${f}"
done

protoc -I . \
  -I proto/third_party \
  --js_out=import_style=commonjs:. \
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. \
  proto/isard.proto

find ./proto -type f -name "*.js" -exec sed -i \
  -e "s~require('\.\./\.\./\.\./\.\./google~require('@/proto/third_party/google~g" \
  -e "s~require('\.\./google~require('@/proto/third_party/google~g" \
  -e "s~require('\.\./\.\./\.\./\.\./protoc-gen-swagger~require('@/proto/third_party/protoc-gen-swagger~g" \
  -e "s~require('\.\./protoc-gen-swagger~require('@/proto/third_party/protoc-gen-swagger~g" \
  {} \;

head -n -3 ./proto/isard_grpc_web_pb.js > ./proto/isard_grpc_web_pb_tmp.js
mv ./proto/isard_grpc_web_pb_tmp.js ./proto/isard_grpc_web_pb.js
echo -e "export default proto.isard\n" >> proto/isard_grpc_web_pb.js

rm -rf src/proto
mv proto src

cd ../backend
