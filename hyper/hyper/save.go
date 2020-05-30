package hyper

import (
	"errors"
	"fmt"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) DesktopSave(id string, savepath string) error {
	desktop, err := h.conn.LookupDomainByName(id)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return ErrDesktopNotStarted

			default:
				return fmt.Errorf("save desktop: %s", e.Message)
			}
		}

		return fmt.Errorf("save desktop: %w", err)
	}
	defer desktop.Free()

	if err := desktop.Save(savepath); err != nil {
		return fmt.Errorf("save desktop: %w", err)
	}
	return nil
}
