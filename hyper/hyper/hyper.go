package hyper

import (
	"fmt"

	"github.com/isard-vdi/isard/hyper/env"

	"libvirt.org/libvirt-go"
)

// Interface is an interface with all the actions that a hypervisor has to be able to do
type Interface interface {
	// Get returns a desktop using it's name
	Get(name string) (*libvirt.Domain, error)

	// Start starts a new machine using the provided XML
	Start(xml string, options *StartOptions) (*libvirt.Domain, error)

	// Stop stops a running desktop
	Stop(desktop *libvirt.Domain) error

	// Suspend suspends a running desktop
	Suspend(desktop *libvirt.Domain) error

	// Resume resumes a suspended desktop
	Resume(desktop *libvirt.Domain) error

	// Save saves a running desktop
	Save(desktop *libvirt.Domain, path string) error

	// Restore restores a saved desktop
	Restore(path string) error

	// XMLGet returns the XML definition of a desktop
	XMLGet(desktop *libvirt.Domain) (string, error)

	// List returns a list of all the running desktops
	List() ([]libvirt.Domain, error)

	// Migrate migrates a running desktop to another hypervisor
	Migrate(desktop *libvirt.Domain, hyperURI string) error

	// Close closes the connection with the hypervisor
	Close() error
}

// Hyper is the implementation of the hyper Interface
type Hyper struct {
	env  *env.Env
	conn *libvirt.Connect
}

// New creates a new Hyper and connects to the libvirt daemon
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

// Close closes the connection with the hypervisor
func (h *Hyper) Close() error {
	_, err := h.conn.Close()
	return err
}
