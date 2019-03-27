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
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"
	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

// UserDesktopsGet returns a list with all the desktops of an user
func (i *IsardServer) UserDesktopsGet(ctx context.Context, req *isard.UserDesktopsGetRequest) (*isard.UserDesktopsGetResponse, error) {
	if md, ok := metadata.FromIncomingContext(ctx); ok {
		if len(md["tkn"]) > 0 {
			tkn := auth.Token(md["tkn"][0])

			if !tkn.CanAccess(req.Id) {
				return &isard.UserDesktopsGetResponse{}, status.Error(codes.PermissionDenied, "you can't access this resource")
			}
		} else {
			return &isard.UserDesktopsGetResponse{}, status.Error(codes.Unauthenticated, "gRPC calls need the token sent through the metadata")
		}
	} else {
		return &isard.UserDesktopsGetResponse{}, status.Error(codes.Unauthenticated, "gRPC calls need the token sent through the metadata")
	}

	d, err := models.GetUserDesktops(req.Id)
	if err != nil {
		return &isard.UserDesktopsGetResponse{}, status.Errorf(codes.Unknown, "error getting the desktop list: %v", err)
	}

	rsp := &isard.UserDesktopsGetResponse{}

	for _, desktop := range d {
		rsp.Desktops = append(rsp.Desktops, &isard.Desktop{
			Id:          desktop.ID,
			Name:        desktop.Name,
			Description: desktop.Description,
			Status:      desktop.Status,
			Detail:      desktop.Detail,
			User:        desktop.User,
			Os:          desktop.OS,
			Options: &isard.DomainOptions{
				Viewers: &isard.DomainOptions_Viewers{
					Spice: &isard.DomainOptions_Viewers_Spice{
						Fullscreen: desktop.Options.Viewers.Spice.Fullscreen,
					},
				},
			},
		})
	}

	return rsp, nil
}
