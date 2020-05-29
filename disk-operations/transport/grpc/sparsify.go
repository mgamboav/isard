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

func (d *DiskOperationsServer) Sparsify(ctx context.Context, req *proto.SparsifyRequest) (*proto.SparsifyResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":         req.Path,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.Sparsify(req.Path)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "sparsify: %v", err)
	}

	return &proto.SparsifyResponse, nil
}
