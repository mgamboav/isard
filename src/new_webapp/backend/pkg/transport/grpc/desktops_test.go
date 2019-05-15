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
	"errors"
	"testing"
	"time"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/transport/grpc"
	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"github.com/dgrijalva/jwt-go"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func TestUserDesktopsGet(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	tkn, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
		Usr: "nefix",
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(
				5 * time.Minute,
			).Unix(),
		},
	}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
	assert.Nil(err)

	t.Run("should return the desktops correctly", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("nefix")).Return([]interface{}{
			map[string]interface{}{
				"id":       "nefix",
				"kind":     "local",
				"role":     "user",
				"password": "$2y$12$8hrQ1UNC2/Y371/uodP/7.L7UAb5B9HjXrndrP5qUHDSuy7P29qVi",
			},
		}, nil)
		mock.On(r.Table("domains").GetAllByIndex("user", "nefix").Filter(
			r.Row.Field("kind").Eq("desktop"),
		)).Return([]interface{}{
			map[string]interface{}{
				"id":          "_nefix_Debian",
				"name":        "Debian",
				"description": "This is a Debian desktop",
				"status":      "STOPPED",
				"detail":      "everything works",
				"user":        "nefix",
				"os":          "linux",
				"options": map[string]interface{}{
					"viewers": map[string]interface{}{
						"spice": map[string]interface{}{
							"fullscreen": true,
						},
					},
				},
			},
			map[string]interface{}{
				"id":          "_nefix_NixOS",
				"name":        "NixOS",
				"description": "This is a NixOS desktop",
				"status":      "FAILED",
				"detail":      "no space left in the disk",
				"user":        "nefix",
				"os":          "linux",
			},
		}, nil)
		db.Session = mock

		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tkn,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		req := &isard.UserDesktopsGetRequest{
			Id: "nefix",
		}

		ctx, err := grpc.CheckAuth(ctx)
		assert.Nil(err)

		expectedRsp := &isard.UserDesktopsGetResponse{
			Desktops: []*isard.Desktop{
				&isard.Desktop{
					Id:          "_nefix_Debian",
					Name:        "Debian",
					Description: "This is a Debian desktop",
					State:       isard.DesktopState_STOPPED,
					Detail:      "everything works",
					User:        "nefix",
					Os:          "linux",
					Options: &isard.DomainOptions{
						Viewers: &isard.DomainOptions_Viewers{
							Spice: &isard.DomainOptions_Viewers_Spice{
								Fullscreen: true,
							},
						},
					},
				},
				&isard.Desktop{
					Id:          "_nefix_NixOS",
					Name:        "NixOS",
					Description: "This is a NixOS desktop",
					State:       isard.DesktopState_FAILED,
					Detail:      "no space left in the disk",
					User:        "nefix",
					Os:          "linux",
					Options: &isard.DomainOptions{
						Viewers: &isard.DomainOptions_Viewers{
							Spice: &isard.DomainOptions_Viewers_Spice{},
						},
					},
				},
			},
		}

		i := grpc.IsardServer{}
		rsp, err := i.UserDesktopsGet(ctx, req)

		assert.Equal(expectedRsp, rsp)
		assert.Nil(err)
	})

	t.Run("should return an error if the user can't access the desktops", func(t *testing.T) {
		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tkn,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		ctx, err := grpc.CheckAuth(ctx)
		assert.Nil(err)

		req := &isard.UserDesktopsGetRequest{
			Id: "usr",
		}

		expectedErr := status.Error(codes.PermissionDenied, "you can't access this resource")

		i := grpc.IsardServer{}
		rsp, err := i.UserDesktopsGet(ctx, req)

		assert.Equal(&isard.UserDesktopsGetResponse{}, rsp)
		assert.Equal(expectedErr, err)
	})

	t.Run("should return an error if there's an error getting the desktops list", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("nefix")).Return([]interface{}{
			map[string]interface{}{
				"id":       "nefix",
				"kind":     "local",
				"role":     "user",
				"password": "$2y$12$8hrQ1UNC2/Y371/uodP/7.L7UAb5B9HjXrndrP5qUHDSuy7P29qVi",
			},
		}, nil)
		mock.On(r.Table("domains").GetAllByIndex("user", "nefix").Filter(
			r.Row.Field("kind").Eq("desktop"),
		)).Return([]interface{}{}, errors.New("testing error"))
		db.Session = mock

		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tkn,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		ctx, err := grpc.CheckAuth(ctx)
		assert.Nil(err)

		req := &isard.UserDesktopsGetRequest{
			Id: "nefix",
		}

		expectedErr := status.Error(codes.Unknown, "error getting the desktop list: error querying the DB: testing error")

		i := grpc.IsardServer{}
		rsp, err := i.UserDesktopsGet(ctx, req)

		assert.Equal(&isard.UserDesktopsGetResponse{}, rsp)
		assert.Equal(expectedErr, err)
	})
}

func TestStartDesktop(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	tkn, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
		Usr: "nefix",
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(
				5 * time.Minute,
			).Unix(),
		},
	}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
	assert.Nil(err)

	t.Run("should start the desktop correctly", func(t *testing.T) {
	})

	t.Run("should return an error if the desktop isn't found", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").Get("_nefix_NixOS")).Return([]interface{}{}, nil)
		db.Session = mock

		ctx := context.Background()
		req := &isard.DesktopStartRequest{
			Id: "_nefix_NixOS",
		}

		expectedRsp := &isard.DesktopStartResponse{}
		expectedErr := status.Errorf(codes.NotFound, "error starting _nefix_NixOS: desktop not found")

		i := grpc.IsardServer{}
		rsp, err := i.DesktopStart(ctx, req)

		assert.Equal(expectedRsp, rsp)
		assert.Equal(expectedErr, err)
	})

	t.Run("should return an error if there's an error getting the desktop from the DB", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").Get("_nefix_NixOS")).Return([]interface{}{}, errors.New("testing error"))
		db.Session = mock

		ctx := context.Background()
		req := &isard.DesktopStartRequest{
			Id: "_nefix_NixOS",
		}

		expectedRsp := &isard.DesktopStartResponse{}
		expectedErr := status.Errorf(codes.Unknown, "error starting _nefix_NixOS: error querying the DB: testing error")

		i := grpc.IsardServer{}
		rsp, err := i.DesktopStart(ctx, req)

		assert.Equal(expectedRsp, rsp)
		assert.Equal(expectedErr, err)
	})

	t.Run("should return an error if the user can't start the desktop (permission denied)", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").Get("_nefix_NixOS")).Return([]interface{}{
			map[string]interface{}{
				"id":          "_nefix_NixOS",
				"name":        "NixOS",
				"description": "This is a NixOS desktop",
				"status":      "FAILED",
				"detail":      "no space left in the disk",
				"user":        "notnefix",
				"os":          "linux",
			},
		}, nil)
		mock.On(r.Table("users").Get("nefix")).Return([]interface{}{
			map[string]interface{}{
				"id":       "nefix",
				"kind":     "local",
				"role":     "user",
				"password": "$2y$12$8hrQ1UNC2/Y371/uodP/7.L7UAb5B9HjXrndrP5qUHDSuy7P29qVi",
			},
		}, nil)
		db.Session = mock

		ctx := context.Background()
		md := metadata.New(map[string]string{
			"tkn": tkn,
		})
		ctx = metadata.NewIncomingContext(ctx, md)

		req := &isard.DesktopStartRequest{
			Id: "_nefix_NixOS",
		}

		expectedRsp := &isard.DesktopStartResponse{}
		expectedErr := status.Errorf(codes.PermissionDenied, "you can't access this resource")

		i := grpc.IsardServer{}
		rsp, err := i.DesktopStart(ctx, req)

		assert.Equal(expectedRsp, rsp)
		assert.Equal(expectedErr, err)
	})

	t.Run("should return an error if there's an error starting the desktop", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").Get("_nefix_NixOS")).Return([]interface{}{
			map[string]interface{}{
				"id":          "_nefix_NixOS",
				"name":        "NixOS",
				"description": "This is a NixOS desktop",
				"status":      "FAILED",
				"detail":      "no space left in the disk",
				"user":        "nefix",
				"os":          "linux",
			},
		}, nil)
		mock.On(r.Table("users").Get("nefix")).Return([]interface{}{
			map[string]interface{}{
				"id":       "nefix",
				"kind":     "local",
				"role":     "user",
				"password": "$2y$12$8hrQ1UNC2/Y371/uodP/7.L7UAb5B9HjXrndrP5qUHDSuy7P29qVi",
			},
		}, nil)
		db.Session = mock

		ctx := context.Background()
		ctx = context.WithValue(ctx, grpc.TokenContextKey, tkn)

		req := &isard.DesktopStartRequest{
			Id: "_nefix_NixOS",
		}

		expectedRsp := &isard.DesktopStartResponse{}
		expectedErr := status.Errorf(codes.Unknown, "error starting _nefix_NixOS: testing error")

		i := grpc.IsardServer{}
		rsp, err := i.DesktopStart(ctx, req)

		assert.Equal(expectedRsp, rsp)
		assert.Equal(expectedErr, err)
	})
}
