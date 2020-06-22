package provider

import (
	"sync"
	"time"

	"github.com/rs/xid"
	"go.uber.org/zap"
)

type PoolInterface interface {
	AddHyper(host string, healthcheck time.Time)
	GetHyper(gpu bool) (string, error)
	RemoveHyper(host string)
	SetHyperMigrating(host string)
	ListHypers() ([]string, map[string]hyper)
}

type Pool struct {
	mux    sync.Mutex
	sugar  *zap.SugaredLogger
	hosts  []string
	hypers map[string]hyper
}

func New(sugar *zap.SugaredLogger) *Pool {
	return &Pool{
		sugar:  sugar,
		hypers: map[string]hyper{},
	}
}

type hyperState int

const (
	hyperStateUnknown hyperState = iota
	hyperStateOK
	hyperStateMigrating
)

type hyper struct {
	id          xid.ID
	state       hyperState
	healthcheck time.Time
}

func (p *Pool) AddHyper(host string, healthcheck time.Time) {
	p.mux.Lock()
	defer p.mux.Unlock()

	if h, ok := p.hypers[host]; ok {
		h.healthcheck = healthcheck
		return
	}

	p.hosts = append(p.hosts, host)
	p.hypers[host] = hyper{
		id:          xid.New(),
		state:       hyperStateOK,
		healthcheck: healthcheck,
	}

	p.sugar.Infow("added hypervisor to the pool",
		"host", host,
	)
}

func (p *Pool) RemoveHyper(host string) {
	p.mux.Lock()
	defer p.mux.Unlock()

	for i, h := range p.hosts {
		if h == host {
			p.hosts = append(p.hosts[:i], p.hosts[i+1:]...)
		}
	}

	if _, ok := p.hypers[host]; ok {
		delete(p.hypers, host)
	}
}

func (p *Pool) SetHyperMigrating(host string) {
	p.mux.Lock()
	defer p.mux.Unlock()

	if _, ok := p.hypers[host]; ok {
		h := p.hypers[host]
		h.state = hyperStateMigrating
		p.hypers[host] = h
	}
}

func (p *Pool) ListHypers() ([]string, map[string]hyper) {
	p.mux.Lock()
	defer p.mux.Unlock()

	return p.hosts, p.hypers
}
