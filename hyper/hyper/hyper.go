package hyper

import (
	"errors"
	"fmt"

	"github.com/isard-vdi/isard/hyper/env"

	"libvirt.org/libvirt-go"
)

var (
	ErrDesktopNotFound = errors.New("desktop not found")
)

type Interface interface {
	Get(name string) (*libvirt.Domain, error)
	Start(xml string, options *StartOptions) (*libvirt.Domain, error)
	Stop(desktop *libvirt.Domain) error
	XMLGet(desktop *libvirt.Domain) (string, error)
	List() ([]libvirt.Domain, error)
	Close() error
}

type Hyper struct {
	env  *env.Env
	conn *libvirt.Connect
}

func New(env *env.Env, uri string) (*Hyper, error) {
	if uri == "" {
		uri = "qemu:///system"
	}

	conn, err := libvirt.NewConnect(uri)
	if err != nil {
		return nil, fmt.Errorf("connect to libvirt: %w", err)
	}

	return &Hyper{env, conn}, nil
}

func (h *Hyper) Close() error {
	_, err := h.conn.Close()
	return err
}
