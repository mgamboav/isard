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

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/transport/grpc"
	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"github.com/stretchr/testify/assert"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func TestLoginLocal(t *testing.T) {
	assert := assert.New(t)

	t.Run("should return a new token if the login is successful", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("nefix")).Return([]interface{}{
			map[string]interface{}{
				"id":       "nefix",
				"kind":     "local",
				"password": "$2y$12$8hrQ1UNC2/Y371/uodP/7.L7UAb5B9HjXrndrP5qUHDSuy7P29qVi",
			},
		}, nil)
		db.Session = mock

		ctx := context.Background()
		req := &isard.LoginLocalRequest{
			Usr: "nefix",
			Pwd: "P4$$w0rd!",
		}

		i := grpc.IsardServer{}
		rsp, err := i.LoginLocal(ctx, req)

		// TODO: Improve this assert
		assert.NotNil(rsp.Tkn)
		assert.Nil(err)
	})

	t.Run("should return an error if there's an error authenticating the user", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("nefix")).Return([]interface{}{}, nil)
		db.Session = mock

		ctx := context.Background()
		req := &isard.LoginLocalRequest{
			Usr: "nefix",
			Pwd: "P4$$w0rd!",
		}

		expectedErr := status.Error(codes.InvalidArgument, "authentication error: error getting the user: user not found")

		i := grpc.IsardServer{}
		rsp, err := i.LoginLocal(ctx, req)

		// TODO: Improve this assert
		assert.Equal(&isard.LoginLocalResponse{}, rsp)
		assert.Equal(expectedErr, err)
	})
}
