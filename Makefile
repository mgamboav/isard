VERSION=2.0.0

all: docker

tidy:
	go mod tidy

docker: tidy
	for microservice in hyper hyper-stats orchestrator disk-operations desktop-builder; do \
		cd $$microservice && make docker VERSION=$(VERSION) ; \
		cd - ; \
	done
