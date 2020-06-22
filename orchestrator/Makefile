VERSION=2.0.0

all: tidy test build docker

tidy:
	go mod tidy

proto: tidy
	protoc -I "." -I pkg/proto/ pkg/proto/orchestrator.proto --go_out=plugins=grpc:pkg/proto
	mv pkg/proto/github.com/isard-vdi/isard/orchestrator/pkg/proto/* pkg/proto
	rm -r pkg/proto/github.com

test: tidy
	go test -race -cover ./...

.PHONY: build
build:
	go build -o orchestrator-bin cmd/orchestrator/main.go

docker: test
	docker build -f build/package/Dockerfile -t isard/orchestrator:${VERSION} ..
