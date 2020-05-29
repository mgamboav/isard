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

func (d *DiskOperationsServer) SnapshotCreate(ctx context.Context, req *proto.SnapshotCreateRequest) (*proto.SnapshotCreateResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
		"id":   req.Id,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.SnapshotCreate(req.Path, req.Id); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot create: %v", err)
	}

	return &proto.SnapshotCreateResponse{}, nil
}

func (d *DiskOperationsServer) SnapshotList(ctx context.Context, req *proto.SnapshotListRequest) (*proto.SnapshotListResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
	}); err != nil {
		return nil, err
	}

	snapshots, err := d.diskoperations.SnapshotList(req.Path)
	if err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot list: %v", err)
	}

	snapshotsproto := &proto.SnapshotListResponse{}
	for _, s := range snapshots {
		snapshotsproto = append(snapshotsproto, &proto.ImageInfoSnapshot{
			Name:          s.Name,
			VmClockNsec:   s.VmClockNsec,
			DateSec:       s.DateSec,
			DateNsec:      s.DateNsec,
			Id:            s.Id,
			s.VmStateSize: s.VmStateSize,
		})
	}

	return snapshotsproto, nil
}

func (d *DiskOperationsServer) SnapshotApply(ctx context.Context, req *proto.SnapshotApplyRequest) (*proto.SnapshotApplyResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
		"id":   req.Id,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.SnapshotApply(req.Path, req.Id, req.Delete); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot apply: %v", err)
	}

	if req.Delete == true {
		//TODO: Delete snapshot after apply
	}

	return &proto.SnapshotApplyResponse{}, nil
}

func (d *DiskOperationsServer) SnapshotDelete(ctx context.Context, req *proto.SnapshotDeleteRequest) (*proto.SnapshotDeleteResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
		"id":   req.Id,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.SnapshotDelete(req.Path, req.Id); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot delete: %v", err)
	}

	return &proto.SnapshotDeleteResponse{}, nil
}
