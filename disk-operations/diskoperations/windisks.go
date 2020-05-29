package diskoperations

import (
	"errors"
	"fmt"
	"os"
	"os/exec"

	"github.com/spf13/afero"
)

func (d *DiskOperations) WinRegistryAdd(name string, regfile *os.File) error {
	if _, err := d.env.FS.Stat(name_input); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("virt-win-reg", name, "--merge", regfile)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("win registry add: %w: %s", err, out)
	}
	return nil
}

func (d *DiskOperations) CopyIn(name string, file *os.File, folder string) error {
	if _, err := d.env.FS.Stat(name_input); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("virt-copy-in", "-a", file, folder)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("win copy in: %w: %s", err, out)
	}
	return nil
}
