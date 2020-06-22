package provider

import (
	"errors"
)

var (
	ErrNoHyperFound = errors.New("no suitable hypervisor was found for the operation")
)

type Provider interface {
	GetHyper(gpu bool) (string, error)
}
