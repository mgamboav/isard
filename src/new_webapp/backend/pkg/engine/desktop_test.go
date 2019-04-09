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

package engine_test

import (
	"context"
	"errors"
	"testing"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/engine"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"
	"github.com/isard-vdi/isard/src/new_webapp/backend/proto/third_party/engine/desktop"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"google.golang.org/grpc"
)

type desktopClientMock struct {
	mock.Mock
}

func (d *desktopClientMock) List(ctx context.Context, req *desktop.ListRequest, opts ...grpc.CallOption) (*desktop.ListResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.ListResponse), args.Error(1)
}

func (d *desktopClientMock) Get(ctx context.Context, req *desktop.GetRequest, opts ...grpc.CallOption) (*desktop.GetResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.GetResponse), args.Error(1)
}

func (d *desktopClientMock) CreateFromTemplate(ctx context.Context, req *desktop.CreateFromTemplateRequest, opts ...grpc.CallOption) (*desktop.CreateFromTemplateResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.CreateFromTemplateResponse), args.Error(1)
}

func (d *desktopClientMock) CreateFromMedia(ctx context.Context, req *desktop.CreateFromMediaRequest, opts ...grpc.CallOption) (*desktop.CreateFromMediaResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.CreateFromMediaResponse), args.Error(1)
}

func (d *desktopClientMock) Update(ctx context.Context, req *desktop.UpdateRequest, opts ...grpc.CallOption) (*desktop.UpdateResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.UpdateResponse), args.Error(1)
}

func (d *desktopClientMock) Delete(ctx context.Context, req *desktop.DeleteRequest, opts ...grpc.CallOption) (*desktop.DeleteResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.DeleteResponse), args.Error(1)
}

func (d *desktopClientMock) Start(ctx context.Context, req *desktop.StartRequest, opts ...grpc.CallOption) (*desktop.StartResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.StartResponse), args.Error(1)
}

func (d *desktopClientMock) Stop(ctx context.Context, req *desktop.StopRequest, opts ...grpc.CallOption) (*desktop.StopResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.StopResponse), args.Error(1)
}

func (d *desktopClientMock) State(ctx context.Context, req *desktop.StateRequest, opts ...grpc.CallOption) (*desktop.StateResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.StateResponse), args.Error(1)
}

func (d *desktopClientMock) Viewer(ctx context.Context, req *desktop.ViewerRequest, opts ...grpc.CallOption) (*desktop.ViewerResponse, error) {
	args := d.Called(ctx, req, opts)
	return args.Get(0).(*desktop.ViewerResponse), args.Error(1)
}

func TestStartDesktop(t *testing.T) {
	assert := assert.New(t)

	t.Run("should start the desktop correctly", func(t *testing.T) {
		theDesktopClientMock := &desktopClientMock{}
		theDesktopClientMock.On("Start", context.Background(), &desktop.StartRequest{DesktopId: "_admin_Debian_9"}, []grpc.CallOption(nil)).Return(
			&desktop.StartResponse{
				State:       desktop.StartResponse_STARTED,
				Detail:      "Successfully started _admin_Debian_9",
				NextActions: []string{"STOP", "VIEWER"},
			}, nil,
		)

		c := engine.Client{
			Desktop: theDesktopClientMock,
		}

		d := &models.Desktop{
			ID:          "_admin_Debian_9",
			Name:        "Debian 9",
			Description: "This is a Debian 9 machine",
			User:        "admin",
		}

		err := c.DesktopStart(d)

		assert.Nil(err)
		assert.Equal("STARTED", d.State)
		assert.Equal("Successfully started _admin_Debian_9", d.Detail)
		assert.Equal([]string{"STOP", "VIEWER"}, d.NextActions)

		theDesktopClientMock.AssertExpectations(t)
	})

	t.Run("should return an error if there's an error starting the desktop", func(t *testing.T) {
		theDesktopClientMock := &desktopClientMock{}
		theDesktopClientMock.On("Start", context.Background(), &desktop.StartRequest{DesktopId: "_admin_Debian_9"}, []grpc.CallOption(nil)).Return(
			&desktop.StartResponse{}, errors.New("disk not found"),
		)

		c := engine.Client{
			Desktop: theDesktopClientMock,
		}

		d := &models.Desktop{
			ID:          "_admin_Debian_9",
			Name:        "Debian 9",
			Description: "This is a Debian 9 machine",
			User:        "admin",
		}

		err := c.DesktopStart(d)

		assert.EqualError(err, "error starting _admin_Debian_9: disk not found")

		theDesktopClientMock.AssertExpectations(t)
	})
}
