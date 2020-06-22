package client

import (
	protoDesktopBuilder "github.com/isard-vdi/isard/desktop-builder/pkg/proto"
	protoOrchestrator "github.com/isard-vdi/isard/orchestrator/pkg/proto"
)

type Client struct {
	DesktopBuilder *protoDesktopBuilder.DesktopBuilderClient
	Orchestrator   *protoOrchestrator.OrchestratorClient
}
