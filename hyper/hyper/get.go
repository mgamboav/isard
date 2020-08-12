package hyper

import (
	"libvirt.org/libvirt-go"
)

// Get returns a desktop using it's name
func (h *Hyper) Get(name string) (*libvirt.Domain, error) {
	desktop, err := h.conn.LookupDomainByName(name)
	if err != nil {
		return nil, err
	}

	return desktop, nil
}
