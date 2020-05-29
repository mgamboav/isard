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

func (d *DiskOperationsServer) InfoQcow2(ctx context.Context, req *proto.InfoQcow2Request) (*proto.InfoQcow2Response, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
	}); err != nil {
		return nil, err
	}

	info, err := d.diskoperations.InfoQcow2(req.Path)
	if err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "info: %v", err)
	}

	snapshots := &[]proto.ImageInfoSnapshot{}
	for _, s := range *info.Snapshots {
		snapshots = append(snapshots, &proto.ImageInfoSnapshot{
			Name:          s.Name,
			VmClockNsec:   s.VmClockNsec,
			DateSec:       s.DateSec,
			DateNsec:      s.DateNsec,
			Id:            s.Id,
			s.VmStateSize: s.VmStateSize,
		})
	}

	infoproto := &proto.InfoQcow2Response{
		Info: &proto.ImageInfoQcow2{
			ActualSize:          info.ActualSize,
			ClusterSize:         info.ClusterSize,
			BackingFilename:     info.BackingFilename,
			DirtyFlag:           info.DirtyFlag,
			Filename:            info.Filename,
			Format:              info.Format,
			FullBackingFilename: info.FullBackingFilename,
			VirtualSize:         info.VirtualSize,
			FormatSpecific: &proto.ImageInfoSpecificQcow2{
				Type: info.FormatSpecific.Type,
				Data: &proto.ImageInfoSpecificQcow2Detail{
					Compat:        info.FormatSpecific.Data.Compat,
					Corrupt:       info.FormatSpecific.Data.Corrupt,
					LazyRefcounts: info.FormatSpecific.Data.LazyRefcounts,
					RefcountBits:  info.FormatSpecific.Data.RefcountBits,
				},
			},
			Snapshots: snapshots,}
		}

	return infoproto, nil
}
