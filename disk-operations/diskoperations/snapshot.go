package diskoperations

import (
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

// TODO: Will always be qcow? or we should check filetypes before proceeding?
func (d *DiskOperations) SnapshotCreate(name string, id string) error {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "snapshot", "-c", id, name)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("create snapshot: %w: %s", err, out)
	}
	return nil
}

func (d *DiskOperations) SnapshotsGet(name string) (*[]ImageInfoSnapshot, error) {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return &[]ImageInfoSnapshot{}, ErrFileNotFound
	}

	if info, err := d.InfoQcow2(name); err != nil {
		return &[]ImageInfoSnapshot{}, fmt.Errorf("get snapshots: %w: %s", err, info)
	}

	return info.Snapshots
}

func (d *DiskOperations) SnapshotApply(name string, id string, delete bool) error {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "snapshot", "-a", id, name)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("apply snapshot: %w: %s", err, out)
	}

	return nil
}

func (d *DiskOperations) SnapshotDelete(name string, id string, delete bool) error {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "snapshot", "-d", id, name)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("delete snapshot: %w: %s", err, out)
	}

	return nil
}
