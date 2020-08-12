package grpc

import (
	"context"

	"github.com/isard-vdi/isard/hyper/pkg/proto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// DesktopList returns a list of the desktops running in the hypervisor
func (h *HyperServer) DesktopList(ctx context.Context, req *proto.DesktopListRequest) (*proto.DesktopListResponse, error) {
	d, err := h.hyper.List()
	if err != nil {
		return nil, status.Error(codes.Unknown, err.Error())
	}

	rsp := &proto.DesktopListResponse{}
	for _, desktop := range d {
		// TODO: Improve error handling
		id, err := desktop.GetName()
		if err == nil {
			rsp.Ids = append(rsp.Ids, id)
		}
	}

	return rsp, nil
}
