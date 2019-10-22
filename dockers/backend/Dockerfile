# Build stage
FROM golang:1.12 as build

COPY ./src/new_webapp/backend /app
WORKDIR /app

RUN GO111MODULE=on CGO_ENABLED=0 go build -a -installsuffix cgo -ldflags '-s -w' -o backend cmd/backend/main.go

# Production stage
FROM alpine:3.8 as production

COPY --from=build /app/backend /backend
RUN mkdir /var/log/isard

VOLUME [ "/etc/isard", "/var/log/isard" ]

CMD [ "/backend" ]

FROM production AS development
