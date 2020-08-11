package hyper

import (
	"errors"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) Get(name string) (*libvirt.Domain, error) {
	desktop, err := h.conn.LookupDomainByName(name)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return nil, ErrDesktopNotFound
			}
		}

		return nil, err
	}

	return desktop, nil
}
