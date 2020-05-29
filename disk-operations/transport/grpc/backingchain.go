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

func (d *DiskOperationsServer) BackingChainQcow2(ctx context.Context, req *proto.BackingChainQcow2Request) (*proto.BackingChainQcow2Response, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path": req.Path,
	}); err != nil {
		return nil, err
	}

	backingchain, err := d.diskoperations.BackingChainQcow2(req.Path)
	if err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}
		if errors.Is(err, diskoperations.ErrBackingFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "backing chain not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "backing chain: %v", err)
	}

	bc := []proto.BackingChainQcow2Response_Path{}
	for _, b := range backingchain {
		bc = append(bc, proto.BackingChainQcow2Response_Path{
			Path: b,
		})
	}

	response := proto.BackingChainQcow2Response{
		Paths: &bc,
	}
	/* 	bc := &proto.BackingChainQcow2Response{}
	   	for _, b := range backingchain {
	   		bc = append(bc, &proto.BackingChainQcow2Response_Path{
	   			Path: b.Path,
	   		})
	   	} */
	return &response, nil
}

func (d *DiskOperationsServer) BackingChainQcow2Replace(ctx context.Context, req *proto.BackingChainQcow2ReplaceRequest) (*proto.BackingChainQcow2ReplaceResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":        req.Path,
		"backingpath": req.Backingpath,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.BackingChainQcow2Replace(req.Path, req.Backingpath); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}
		if errors.Is(err, diskoperations.ErrBackingFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "backing chain not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "backing chain replace: %v", err)
	}

	return &proto.BackingChainQcow2ReplaceResponse{}, nil
}

func (d *DiskOperationsServer) BackingChainQcow2Rebase(ctx context.Context, req *proto.BackingChainQcow2RebaseRequest) (*proto.BackingChainQcow2RebaseResponse, error) {
	if err := grpc.Required(grpc.RequiredParams{
		"path":        req.Path,
		"backingpath": req.Backingpath,
	}); err != nil {
		return nil, err
	}

	if err := d.diskoperations.BackingChainQcow2Rebase(req.Path, req.Backingpath, req.DeleteIntermediates); err != nil {
		if errors.Is(err, diskoperations.ErrFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "path not found: %v", err)
		}
		if errors.Is(err, diskoperations.ErrBackingFileNotFound) {
			return nil, status.Errorf(codes.NotFound, "backing chain not found: %v", err)
		}

		return nil, status.Errorf(codes.Unknown, "backing chain rebase: %v", err)
	}

	return &proto.BackingChainQcow2RebaseResponse{}, nil
}
