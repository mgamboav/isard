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

package grpc

import (
	"context"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

// ContextKey is a key in the context
type ContextKey string

// TokenContextKey is the key that contains the token
const TokenContextKey ContextKey = "tkn"

// CheckAuth checks if the user is authenticated
func CheckAuth(ctx context.Context) (context.Context, error) {
	if md, ok := metadata.FromIncomingContext(ctx); ok {
		if len(md["tkn"]) > 0 {
			tkn := auth.Token(md["tkn"][0])
			if !tkn.Validate() {
				return ctx, status.Errorf(codes.InvalidArgument, "invalid token")
			}

			ctx = context.WithValue(ctx, TokenContextKey, tkn)
			return ctx, nil
		}
	}

	return ctx, status.Errorf(codes.Unauthenticated, "gRPC calls need the token sent through the metadata")
}

// canAccess checks if an user can access to a specific resource
func canAccess(ctx context.Context, id string) error {
	tkn, ok := ctx.Value(TokenContextKey).(auth.Token)
	if !ok || !tkn.CanAccess(id) {
		return status.Error(codes.PermissionDenied, "you can't access this resource")
	}

	return nil
}

// IsardServer is the implementation of the gRPC Isard service
type IsardServer struct{}
