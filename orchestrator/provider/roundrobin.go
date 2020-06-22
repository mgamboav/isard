package provider

import "time"

type RoundRobin struct {
	Pool PoolInterface
}

// TODO: Actually make it round robin
func (r *RoundRobin) GetHyper(gpu bool) (string, error) {
	hosts, hypers := r.Pool.ListHypers()

	for _, h := range hosts {
		hyper := hypers[h]

		if hyper.healthcheck.Before(time.Now().Add(-10 * time.Second)) {
			r.Pool.RemoveHyper(h)
			continue
		}

		if hyper.state == hyperStateOK {
			return h, nil
		}
	}

	return "", ErrNoHyperFound
}
