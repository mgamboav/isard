# Build stage
FROM golang:1.12 as build-stage

COPY ./src/new_webapp/backend /app
WORKDIR /app

RUN GO111MODULE=on CGO_ENABLED=0 go build -a -installsuffix cgo -ldflags '-s -w' -o backend cmd/backend/main.go

# Production stage
FROM alpine:3.8 as production-stage

COPY --from=build-stage /app/backend /backend

VOLUME /etc/isard
VOLUME /backend.log

CMD [ "/backend" ]
