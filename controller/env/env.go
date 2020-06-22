package env

import (
	"sync"

	"go.uber.org/zap"
)

type Env struct {
	WG    sync.WaitGroup
	Sugar *zap.SugaredLogger
}
