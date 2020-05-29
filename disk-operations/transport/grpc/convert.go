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

func (d *DiskOperationsServer) Convert(ctx context.Context, req *proto.ConvertRequest) (*proto.ConvertResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path_input":	req.path,
		"path_output":	req.path_input,
		"format_input":	req.format_input,
		"format_output":req.format_output,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.Convert(req.path_input, req.path_output, req.format_input, req.format_output)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "backing chain: %v", err)
	}

	return &proto.ConvertResponse{}, nil
}
