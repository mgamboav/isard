FROM golang:1.12 as build

COPY backend /go/src/github.com/isard-vdi/isard/src/new_webapp/backend

# Move to the correct directory
WORKDIR /go/src/github.com/isard-vdi/isard/src/new_webapp/backend

# Compile the binary
RUN GO111MODULE=on go build -o isard cmd/backend/main.go

#
# Base stage
#

# Use alpine 3.8 as base
FROM alpine:3.8

# Copy the compiled binary from the build stage
COPY --from=build /go/src/github.com/isard-vdi/isard/src/new_webapp/backend/isard /app/isard

# Move to the correct directory
WORKDIR /data

# Expose the volume
VOLUME [ "/data" ]

# Expose the required port
EXPOSE 3000

# Run the service
CMD [ "/app/isard" ]
