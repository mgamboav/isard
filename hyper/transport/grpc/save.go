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

func (h *HyperServer) DesktopSave(ctx context.Context, req *proto.DesktopSaveRequest) (*proto.DesktopSaveResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"id":       req.Id,
		"savepath": req.Savepath,
	}); err != nil {
		return nil, err
	}

	if err := h.hyper.DesktopSave(req.Id, req.Savepath); err != nil {
		if errors.Is(err, hyper.ErrDesktopNotStarted) {
			return nil, status.Errorf(codes.FailedPrecondition, "save desktop: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "save desktop: %v", err)
	}

	return &proto.DesktopSaveResponse{}, nil
}
