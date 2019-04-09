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

package grpc_test

import (
	"context"
	"testing"
	"time"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/transport/grpc"

	"github.com/dgrijalva/jwt-go"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

func TestCheckAuth(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.SetDefaults()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	t.Run("shouldn't return any error if the token is valid", func(t *testing.T) {
		tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
			Usr: "nefix",
			StandardClaims: jwt.StandardClaims{
				ExpiresAt: time.Now().Add(
					5 * time.Minute,
				).Unix(),
			},
		}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
		assert.Nil(err)

		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tknStr,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		ctx, err = grpc.CheckAuth(ctx)
		assert.Nil(err)

		assert.Equal(tknStr, ctx.Value(grpc.TokenContextKey).(auth.Token).String())
	})

	t.Run("should return an error if no metadata is provided", func(t *testing.T) {
		ctx := context.Background()

		expectedErr := status.Error(codes.Unauthenticated, "gRPC calls need the token sent through the metadata")

		_, err := grpc.CheckAuth(ctx)

		assert.Equal(expectedErr, err)
	})

	t.Run("should return an error if the token header isn't provided", func(t *testing.T) {
		ctx := context.Background()
		md := metadata.New(map[string]string{})
		ctx = metadata.NewIncomingContext(ctx, md)

		expectedErr := status.Error(codes.Unauthenticated, "gRPC calls need the token sent through the metadata")

		_, err := grpc.CheckAuth(ctx)

		assert.Equal(expectedErr, err)
	})

	t.Run("should return an error if the token is invalid", func(t *testing.T) {
		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": "token",
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		expectedErr := status.Error(codes.InvalidArgument, "invalid token")

		_, err := grpc.CheckAuth(ctx)

		assert.Equal(expectedErr, err)
	})
}
