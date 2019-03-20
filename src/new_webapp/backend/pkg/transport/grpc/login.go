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
	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// LoginLocal logs in the user using the local database and returns the token
func (i *IsardServer) LoginLocal(ctx context.Context, req *isard.LoginLocalRequest) (*isard.LoginLocalResponse, error) {
	tkn, err := auth.LoginLocal(req.Usr, req.Pwd)
	if err != nil {
		return nil, status.Errorf(codes.InvalidArgument, "authentication error: %v", err)
	}

	return &isard.LoginLocalResponse{Tkn: tkn.String()}, nil
}
