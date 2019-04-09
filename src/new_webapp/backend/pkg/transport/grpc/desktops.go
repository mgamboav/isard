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

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/engine"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"
	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// parseState returns the Desktop state from a string
func parseState(strState string) isard.Desktop_State {
	state := isard.Desktop_State(isard.Desktop_State_value[strState])

	// if the state isn't found, the map is going to return 0, which is the stopped status
	if state == 0 {
		if strState != isard.Desktop_State_name[0] {
			state = isard.Desktop_UNKNOWN
		}
	}

	return state
}

// UserDesktopsGet returns a list with all the desktops of an user
func (i *IsardServer) UserDesktopsGet(ctx context.Context, req *isard.UserDesktopsGetRequest) (*isard.UserDesktopsGetResponse, error) {
	if err := canAccess(ctx, req.Id); err != nil {
		return &isard.UserDesktopsGetResponse{}, err
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
			State:       parseState(desktop.State),
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

// DesktopStart starts a desktop
func (i *IsardServer) DesktopStart(ctx context.Context, req *isard.DesktopStartRequest) (*isard.DesktopStartResponse, error) {
	d, err := models.GetDesktop(req.Id)
	if err != nil {
		if err.Error() == "desktop not found" {
			return &isard.DesktopStartResponse{}, status.Errorf(codes.NotFound, "error starting %s: %v", req.Id, err)
		}

		return &isard.DesktopStartResponse{}, status.Errorf(codes.Unknown, "error starting %s: %v", req.Id, err)
	}

	if err := canAccess(ctx, d.User); err != nil {
		return &isard.DesktopStartResponse{}, err
	}

	if err := engine.Cli.DesktopStart(d); err != nil {
		return &isard.DesktopStartResponse{}, status.Errorf(codes.Unknown, "error starting %s: %v", req.Id, err)
	}

	return &isard.DesktopStartResponse{
		State:       d.State,
		NextActions: d.NextActions,
	}, nil
}
