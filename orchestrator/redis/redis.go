package redis

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"time"

	"github.com/go-redis/redis/v7"
	hypRedis "github.com/isard-vdi/isard/hyper-stats/pkg/redis"
	"github.com/isard-vdi/isard/orchestrator/env"
	"github.com/isard-vdi/isard/orchestrator/provider"
)

func Init(env *env.Env, pool provider.PoolInterface) {
	env.Redis = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", env.Cfg.Redis.Host, env.Cfg.Redis.Port),
		Password: env.Cfg.Redis.Password,
	})

	_, err := env.Redis.Ping().Result()
	if err != nil {
		env.Sugar.Fatalw("connect to redis",
			"err", err,
		)
	}

	env.WG.Add(1)
	go listenHyperConnections(env, pool)

	// Wait to recieve messages of all the availabe hypers before starting
	time.Sleep(10 * time.Second)
}

func listenHyperConnections(env *env.Env, pool provider.PoolInterface) {
	sub := env.Redis.Subscribe(hypRedis.Channel)
	ch := sub.Channel()

	for {
		select {
		case msg := <-ch:
			var h hypRedis.HyperMsg
			buf := bytes.NewBufferString(msg.Payload)
			if err := gob.NewDecoder(buf).Decode(&h); err != nil {
				env.Sugar.Errorw("decode hyper message",
					"err", err,
					"payload", msg.Payload,
				)
				break
			}

			switch h.State {
			case hypRedis.HyperStateOK:
				pool.AddHyper(h.Host, h.Time)

			case hypRedis.HyperStateMigrating:
				pool.SetHyperMigrating(h.Host)

			case hypRedis.HyperStateStopping:
				pool.RemoveHyper(h.Host)

			default:
				env.Sugar.Errorw("unknown hyper state",
					"state", h.State,
				)

				pool.RemoveHyper(h.Host)
			}

		case <-env.Ctx.Done():
			sub.Close()

			env.WG.Done()
			return
		}
	}
}
