package hyper

import (
	"fmt"

	"github.com/isard-vdi/isard/hyper/env"

	"libvirt.org/libvirt-go"
)

// Interface is an interface with all the actions that a hypervisor has to be able to do
type Interface interface {
	// Get returns a running desktop object from it's name
	Get(name string) (*libvirt.Domain, error)

	// Start starts a new machine using the provided XML definition
	// so it is a non-persistent desktop from libvirt point of view
	Start(xml string, options *StartOptions) (*libvirt.Domain, error)

	// Stop stops a running desktop
	Stop(desktop *libvirt.Domain) error

	// Suspend suspends a running desktop temporarily saving its memory state. It won't persist hypervisor restarts.
	Suspend(desktop *libvirt.Domain) error

	// Resume resumes a suspended desktop to its original running state, continuingly execution where it left off.
	Resume(desktop *libvirt.Domain) error

	// Save saves a running desktop saving its memory state to a file. Will persiste hypervisor restart.
	Save(desktop *libvirt.Domain, path string) error

	// Restore restores a saved desktop to its original running state, continuing execution where it left off.
	Restore(path string) error

	// XMLGet returns the running XML definition of a running desktop, so it will have running parameters.
	XMLGet(desktop *libvirt.Domain) (string, error)

	// List returns a list of all the running desktops names.
	List() ([]libvirt.Domain, error)

	// Migrate migrates a running desktop to another hypervisor using PEER2PEER method
	Migrate(desktop *libvirt.Domain, hyperURI string) error

	// Close closes the libvirt connection with the hypervisor
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