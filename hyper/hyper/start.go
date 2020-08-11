package hyper

import (
	"errors"
	"fmt"

	"libvirt.org/libvirt-go"
)

type StartOptions struct {
	Paused bool
}

// Start starts a new machine using the provided XML
func (h *Hyper) Start(xml string, options *StartOptions) (*libvirt.Domain, error) {
	flag := libvirt.DOMAIN_NONE
	if options.Paused {
		flag = libvirt.DOMAIN_START_PAUSED
	}

	desktop, err := h.conn.DomainCreateXML(xml, flag)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_XML_ERROR, libvirt.ERR_XML_DETAIL:
				return nil, fmt.Errorf("create desktop: %w", e)

			default:
				return nil, fmt.Errorf("create desktop: %s", e.Message)
			}
		}

		return nil, fmt.Errorf("create desktop: %w", err)
	}

	return desktop, nil
}
