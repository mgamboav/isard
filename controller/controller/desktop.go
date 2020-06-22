package controller

import (
	"context"

	"github.com/isard-vdi/isard/desktop-builder/desktopbuilder"
	"github.com/isard-vdi/isard/desktop-builder/pkg/proto"
)

func (c *Controller) DesktopStart(ctx context.Context, id string) (*desktopbuilder.Viewer, error) {
	rsp, err := c.client.Orchestrator.

	rsp, err := c.client.DesktopBuilder.XMLGet(ctx, &proto.XMLGetRequest{
		Id: id,
	})
	if err != nil {
		return nil, err
	}
}
