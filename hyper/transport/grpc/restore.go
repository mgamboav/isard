package grpc

import (
	"context"
	"errors"

	"github.com/isard-vdi/isard/common/pkg/grpc"
	"github.com/isard-vdi/isard/hyper/pkg/proto"
	"github.com/spf13/afero"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// DesktopResume resumes a suspended desktop in the hypervisor
func (h *HyperServer) DesktopRestore(ctx context.Context, req *proto.DesktopRestoreRequest) (*proto.DesktopRestoreResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
	}); err != nil {
		return nil, err
	}

	if err := h.hyper.Restore(req.Path); err != nil {
		return nil, status.Error(codes.Unknown, err.Error())
	}

	if err := h.env.FS.Remove(req.Path); err != nil {
		if !errors.Is(err, afero.ErrFileNotFound) {
			return nil, status.Error(codes.NotFound, err.Error())
		}
	}

	return &proto.DesktopRestoreResponse{}, nil
}
