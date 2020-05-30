package hyper

import (
	"errors"
	"fmt"

	"libvirt.org/libvirt-go"
)

var (
	ErrDesktopNotMigrated     = errors.New("desktop not migrated")
	ErrDesktopMigrationUnsafe = errors.New("desktop migration unsafe")
)

func (h *Hyper) DesktopMigrateLive(id string, hypervisor string, bandwidth uint64) error {
	desktop, err := h.conn.LookupDomainByName(id)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return ErrDesktopNotStarted

			default:
				return fmt.Errorf("migrate desktop: %s", e.Message)
			}
		}

		return fmt.Errorf("migrate desktop: %w", err)
	}
	defer desktop.Free()

	err = desktop.MigrateToURI(fmt.Sprintf("qemu+ssh://%s/system", hypervisor), libvirt.MIGRATE_LIVE, id, bandwidth)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_MIGRATE_UNSAFE:
				return ErrDesktopMigrationUnsafe

			default:
				return fmt.Errorf("migrate desktop: %s", e.Message)
			}
		}

		return fmt.Errorf("migrate desktop: %w", err)
	}
	return nil
}
