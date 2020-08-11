package hyper

import (
	"errors"
	"fmt"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) Stop(desktop *libvirt.Domain) error {
	if err := desktop.Destroy(); err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return ErrDesktopNotFound
			default:
				return fmt.Errorf("stop desktop: %s", e.Message)
			}
		}

		return fmt.Errorf("stop desktop: %w", err)
	}

	return nil
}
