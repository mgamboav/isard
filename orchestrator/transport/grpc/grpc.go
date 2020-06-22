package grpc

import (
	"context"
	"fmt"
	"net"

	"github.com/isard-vdi/isard/orchestrator/env"
	"github.com/isard-vdi/isard/orchestrator/pkg/proto"

	gRPC "google.golang.org/grpc"
)

// API is the version for the gRPC API
const API = "v1.0.0"

// OrchestratorServer implements teh gRPC server
type OrchestratorServer struct {
	env *env.Env
}

func Serve(ctx context.Context, env *env.Env) {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", env.Cfg.GRPC.Port))
	if err != nil {
		env.Sugar.Fatalw("listen gRPC port",
			"err", err,
			"port", env.Cfg.GRPC.Port,
		)
	}

	srv := &OrchestratorServer{env}
	s := gRPC.NewServer()
	proto.RegisterOrchestratorServer(s, srv)

	env.Sugar.Infow("Orchestrator gRPC serving",
		"port", env.Cfg.GRPC.Port,
	)
	go func() {
		if err = s.Serve(lis); err != nil {
			if err != gRPC.ErrServerStopped {
				env.Sugar.Fatalw("serve Orchestrator gRPC",
					"err", err,
					"port", env.Cfg.GRPC.Port,
				)
			}
		}
	}()

	select {
	case <-ctx.Done():
		s.Stop()
		env.WG.Done()
	}
}
