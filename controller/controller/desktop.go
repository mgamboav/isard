package controller

import (
	"context"
	"errors"

	"github.com/go-redis/redis/v7"

	"github.com/isard-vdi/isard/desktop-builder/desktopbuilder"
	"github.com/isard-vdi/isard/desktop-builder/pkg/proto"
)

func (c *Controller) DesktopStart(ctx context.Context, id string) (*desktopbuilder.Viewer, error) {
	// Check if the desktop is already started
	if err := redis.GetDesktop(c.env, id); err != nil {
		if errors.Is(redis.Nil)
	}

	rsp, err := c.client.DesktopBuilder.XMLGet(ctx, &proto.XMLGetRequest{
		Id: id,
	})
	if err != nil {
		return nil, err
	}

	// Ask for the hypervisor

	// Prepare the disk

	// Start the desktop
}
