package grpc

import (
	"context"
	"errors"

	"github.com/isard-vdi/isard/common/pkg/grpc"
	"github.com/isard-vdi/isard/hyper/hyper"
	"github.com/isard-vdi/isard/hyper/pkg/proto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (h *HyperServer) DesktopRestore(ctx context.Context, req *proto.DesktopRestoreRequest) (*proto.DesktopRestoreResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"id": req.Savepath,
	}); err != nil {
		return nil, err
	}

	if err := h.hyper.DesktopRestore(req.Savepath); err != nil {
		if errors.Is(err, hyper.ErrDesktopNotStarted) {
			return nil, status.Errorf(codes.FailedPrecondition, "resume desktop: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "resume desktop: %v", err)
	}

	return &proto.DesktopRestoreResponse{}, nil
}
