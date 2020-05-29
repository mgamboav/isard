package diskoperations

import (
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

// TODO: Will always be qcow? or we should check filetypes before proceeding?
func (d *DiskOperations) Sparsify(name string) error {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("virt-sparsify", "--in-place", name)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("convert image: %w: %s", err, out)
	}
	return nil
}
