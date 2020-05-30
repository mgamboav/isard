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

func (h *HyperServer) DesktopScreenshot(ctx context.Context, req *proto.DesktopScreenshotRequest) (*proto.DesktopScreenshotResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"id": req.Id,
	}); err != nil {
		return nil, err
	}

	if screen, err := h.hyper.DesktopScreenshot(req.Id); err != nil {
		if errors.Is(err, hyper.ErrDesktopNotStarted) {
			return nil, status.Errorf(codes.FailedPrecondition, "desktop screenshot: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "desktop screenshot: %v", err)
	}

	return &proto.DesktopScreenshotResponse{}, nil
}
