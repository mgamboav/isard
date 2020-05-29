package grpc

import (
	"context"
	"errors"

	"github.com/isard-vdi/isard/common/pkg/grpc"
	"github.com/isard-vdi/isard/disk-operations/diskoperations"
	"github.com/isard-vdi/isard/disk-operations/pkg/proto"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (d *DiskOperationsServer) InfoQcow2(ctx context.Context, req *proto.InfoQcow2Request) (*proto.InfoQcow2Response, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":         req.Path,
	}); err != nil {
		return nil, err
	}

	if info, err := d.diskoperations.InfoQcow2(req.Path)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "info: %v", err)
	}

	return info, nil
}
