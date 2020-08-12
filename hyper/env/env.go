package env

import (
	"sync"

	"github.com/isard-vdi/isard/hyper/cfg"
	"github.com/spf13/afero"

	"go.uber.org/zap"
)

type Env struct {
	WG    sync.WaitGroup
	Sugar *zap.SugaredLogger

	FS  afero.Fs
	Cfg cfg.Cfg
}
