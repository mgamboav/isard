package env

import (
	"sync"

	"github.com/isard-vdi/isard/controller/cfg"

	"github.com/go-redis/redis/v7"
	"go.uber.org/zap"
)

type Env struct {
	WG    sync.WaitGroup
	Sugar *zap.SugaredLogger

	Cfg   cfg.Cfg
	Redis *redis.Client
}
