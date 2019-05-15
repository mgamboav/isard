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
	"testing"
	"time"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"

	"github.com/dgrijalva/jwt-go"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func TestCanAccess(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.SetDefaults()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
		Usr: "nefix",
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(
				5 * time.Minute,
			).Unix(),
		},
	}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
	assert.Nil(err)

	mock := r.NewMock()
	mock.On(r.Table("users").Get("nefix")).Return([]interface{}{
		map[string]interface{}{
			"id": "nefix",
		},
	}, nil)
	mock.On(r.Table("users").Get("notnefix")).Return([]interface{}{
		map[string]interface{}{
			"id": "notnefix",
		},
	}, nil)
	db.Session = mock

	t.Run("should return no error if the user can access the resource", func(t *testing.T) {
		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tknStr,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		ctx, err = CheckAuth(ctx)
		assert.Nil(err)

		assert.Nil(canAccess(ctx, "nefix"))
	})

	t.Run("should return an error if the user is unauthenticated", func(t *testing.T) {
		ctx := context.Background()

		assert.Equal(canAccess(ctx, "notnefix"), status.Error(codes.PermissionDenied, "you can't access this resource"))
	})

	t.Run("should return an error if the user can't access the resource", func(t *testing.T) {
		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tknStr,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		ctx, err = CheckAuth(ctx)
		assert.Nil(err)

		assert.Equal(canAccess(ctx, "notnefix"), status.Error(codes.PermissionDenied, "you can't access this resource"))
	})
}
