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

func (h *HyperServer) DesktopXMLGet(ctx context.Context, req *proto.DesktopXMLGetRequest) (*proto.DesktopXMLGetResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"id": req.Id,
	}); err != nil {
		return nil, err
	}

	desktop, err := h.hyper.Get(req.Id)
	if err != nil {
		if errors.Is(err, hyper.ErrDesktopNotFound) {
			return nil, status.Errorf(codes.NotFound, "get desktop XML: get desktop: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "get desktop XML: get desktop: %v", err)
	}
	defer desktop.Free()

	xml, err := h.hyper.XMLGet(desktop)
	if err != nil {
		return nil, status.Errorf(codes.Unknown, "get XML: %v", err)
	}

	return &proto.DesktopXMLGetResponse{Xml: xml}, nil
}
