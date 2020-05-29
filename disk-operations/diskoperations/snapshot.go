package diskoperations

import (
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

// TODO: Will always be qcow? or we should check filetypes before proceeding?
func (d *DiskOperations) SnapshotCreate(path string, id string) error {
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "snapshot", "-c", id, path)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("create snapshot: %w: %s", err, out)
	}
	return nil
}

func (d *DiskOperations) SnapshotList(path string) (*[]ImageInfoSnapshot, error) {
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return &[]ImageInfoSnapshot{}, ErrFileNotFound
	}

	info, err := d.InfoQcow2(path)
	if err != nil {
		return &[]ImageInfoSnapshot{}, fmt.Errorf("get snapshots: %w", err)
	}

	return info.Snapshots, nil
}

func (d *DiskOperations) SnapshotApply(path string, id string, delete bool) error {
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "snapshot", "-a", id, path)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("apply snapshot: %w: %s", err, out)
	}

	return nil
}

func (d *DiskOperations) SnapshotDelete(path string, id string) error {
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "snapshot", "-d", id, path)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("delete snapshot: %w: %s", err, out)
	}

	return nil
}
