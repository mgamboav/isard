#!/bin/sh

protoc -I . \
  -I $GOPATH/src \
  -I $GOPATH/pkg/mod/github.com/grpc-ecosystem/grpc-gateway@v1.7.0/third_party/googleapis \
  --grpc-gateway_out=logtostderr=true:. \
  --go_out=plugins=grpc:. \
  --swagger_out=logtostderr=true:. \
  proto/isard.proto