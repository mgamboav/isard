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

func (h *HyperServer) DesktopStop(ctx context.Context, req *proto.DesktopStopRequest) (*proto.DesktopStopResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"id": req.Id,
	}); err != nil {
		return nil, err
	}

	desktop, err := h.hyper.Get(req.Id)
	if err != nil {
		if errors.Is(err, hyper.ErrDesktopNotFound) {
			return nil, status.Errorf(codes.FailedPrecondition, "stop desktop: get desktop: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "stop desktop: get desktop: %v", err)
	}
	defer desktop.Free()

	if err := h.hyper.Stop(desktop); err != nil {
		return nil, status.Errorf(codes.Unknown, "stop desktop: %v", err)
	}

	return &proto.DesktopStopResponse{}, nil
}
