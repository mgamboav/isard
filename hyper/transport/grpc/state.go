package grpc

import (
	"context"
	"errors"

	"github.com/isard-vdi/isard/common/pkg/grpc"
	"github.com/isard-vdi/isard/hyper/pkg/proto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"libvirt.org/libvirt-go"
)

// DesktopResume resumes a suspended desktop in the hypervisor
func (h *HyperServer) DesktopState(ctx context.Context, req *proto.DesktopStateRequest) (*proto.DesktopStateResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"id": req.Id,
	}); err != nil {
		return nil, err
	}

	desktop, err := h.hyper.Get(req.Id)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return nil, status.Error(codes.NotFound, "desktop not found")
			}
		}

		return nil, status.Errorf(codes.Unknown, "get desktop: %v", err)
	}
	defer desktop.Free()

	state, _, err := desktop.GetState()
	if state == libvirt.DOMAIN_NOSTATE {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Nostate,
		}, nil
	} else if state == libvirt.DOMAIN_RUNNING {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Started,
		}, nil
	} else if state == libvirt.DOMAIN_BLOCKED {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Blocked,
		}, nil
	} else if state == libvirt.DOMAIN_PAUSED {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Paused,
		}, nil
	} else if state == libvirt.DOMAIN_SHUTDOWN {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Stopping,
		}, nil
	} else if state == libvirt.DOMAIN_SHUTOFF {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Stopped,
		}, nil
	} else if state == libvirt.DOMAIN_CRASHED {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Crashed,
		}, nil
	} else if state == libvirt.DOMAIN_PMSUSPENDED {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Suspended,
		}, nil
	} else {
		return &proto.DesktopStateResponse{
			State: proto.DesktopStateResponse_Unknown,
		}, nil
	}

	return &proto.DesktopStateResponse{}, nil
}
