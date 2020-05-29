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
		"path_input":    req.PathInput,
		"path_output":   req.PathOutput,
		"format_input":  req.FormatInput,
		"format_output": req.FormatOutput,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.Convert(req.PathInput, req.PathOutput, req.FormatInput, req.FormatOutput); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "backing chain: %v", err)
	}

	return &proto.ConvertResponse{}, nil
}
