/*
 * Copyright (C) 2019 IsardVDI
 * Authors: IsardVDI Authors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package main

import (
	"context"
	"log"
	"net"

	isardGRPC "github.com/isard-vdi/isard/src/new_webapp/backend/pkg/transport/grpc"
	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"google.golang.org/grpc"
)

// TODO: API version check

// unaryInterceptor intercepts the gRPC Unary calls and does actions with them before continuing (or returning an error)
func unaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	// don't check for the token if it's a login method
	if info.FullMethod != "/isard.Isard/LoginLocal" {
		if err := isardGRPC.CheckToken(ctx); err != nil {
			return nil, err
		}
	}

	return handler(ctx, req)
}

// streamInterceptor intercepts the gRPC Stream calls and does actions with them before continuing (or returning an error)
func streamInterceptor(srv interface{}, stream grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
	if err := isardGRPC.CheckToken(stream.Context()); err != nil {
		return err
	}

	return handler(srv, stream)
}

func main() {
	lis, err := net.Listen("tcp", ":1312")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	grpcServer := grpc.NewServer(
		grpc.UnaryInterceptor(unaryInterceptor),
		grpc.StreamInterceptor(streamInterceptor),
	)

	isard.RegisterIsardServer(grpcServer, &isardGRPC.IsardServer{})

	log.Println("Isard listening at port :1312...")
	if err = grpcServer.Serve(lis); err != nil {
		log.Fatalf("error serving Isard: %v", err)
	}
}
