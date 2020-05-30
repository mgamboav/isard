package hyper

import (
	"errors"
	"fmt"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) DesktopSuspend(id string) error {
	desktop, err := h.conn.LookupDomainByName(id)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return ErrDesktopNotStarted

			default:
				return fmt.Errorf("suspend desktop: %s", e.Message)
			}
		}

		return fmt.Errorf("suspend desktop: %w", err)
	}
	defer desktop.Free()

	if err := desktop.Suspend(); err != nil {
		return fmt.Errorf("suspend desktop: %w", err)
	}
	return nil
}
