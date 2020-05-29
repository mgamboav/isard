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
		"path":         req.Path,
		"id":			req.Id,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.SnapshotCreate(req.Path, req.Id)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot create: %v", err)
	}

	return &proto.SnapshotCreateResponse{}, nil
}

func (d *DiskOperationsServer) SnapshotList(ctx context.Context, req *proto.SnapshotListRequest) (*proto.SnapshotListResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":         req.Path,
	}); err != nil {
		return nil, err
	}

	if snapshots, err := d.diskoperations.SnapshotList(req.Path)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot list: %v", err)
	}

	return snapshots, nil
}

func (d *DiskOperationsServer) SnapshotApply(ctx context.Context, req *proto.SnapshotApplyRequest) (*proto.SnapshotApplyResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":         req.Path,
		"id":			req.Id,
	}); err != nil {
		return nil, err
	}

	if req.Delete == nil {
		req.Delete = false
	}

	if err := d.diskoperations.SnapshotApply(req.Path, req.Id, req.Delete)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot apply: %v", err)
	}

	return &proto.SnapshotApplyResponse{}, nil
}

func (d *DiskOperationsServer) SnapshotDelete(ctx context.Context, req *proto.SnapshotDeleteRequest) (*proto.SnapshotDeleteResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":         req.Path,
		"id":			req.Id,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.SnapshotDelete(req.Path, req.Id)); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound)  {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "snapshot delete: %v", err)
	}

	return &proto.SnapshotDeleteResponse{}, nil
}