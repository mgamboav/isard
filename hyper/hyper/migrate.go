package hyper

import "libvirt.org/libvirt-go"

func (h *Hyper) Migrate(d *libvirt.Domain, hyper string) error {
	name, err := d.GetName()
	if err != nil {
		panic(err)
	}

	if err := d.MigrateToURI(hyper, libvirt.MIGRATE_PEER2PEER, name, 0); err != nil {
		panic(err)
	}

	return nil
}
