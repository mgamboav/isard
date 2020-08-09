package redis

import (
	"fmt"

	"github.com/go-redis/redis/v7"
	"github.com/isard-vdi/isard/controller/env"
)

func Init(env *env.Env) {
	env.Redis = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", env.Cfg.Redis.Host, env.Cfg.Redis.Port),
		Password: env.Cfg.Redis.Password,
	})

	if _, err := env.Redis.Ping().Result(); err != nil {
		env.Sugar.Fatalw("connect to redis",
			"err", err,
		)
	}

	env.WG.Add(1)
}

func GetDesktop(env *env.Env, id string) error {
	_, err := env.Redis.Get("desktop_" + id).Result()

	return err
}
