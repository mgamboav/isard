VERSION=2.0.0

all: tidy proto test build docker

tidy:
	go mod tidy

proto: tidy
	protoc -I "." -I pkg/proto/ pkg/proto/controller.proto --go_out=plugins=grpc:pkg/proto
	mv pkg/proto/github.com/isard-vdi/isard/controller/pkg/proto/* pkg/proto
	rm -r pkg/proto/github.com

test: proto
	go test -race -cover ./...

.PHONY: build
build:
	go build -o controller-bin cmd/controller/main.go

docker: test
	docker build -f build/package/Dockerfile -t isard/controller:${VERSION} ..
