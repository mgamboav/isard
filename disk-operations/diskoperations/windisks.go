package diskoperations

/* import (
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

func (d *DiskOperations) WinRegistryAdd(name string, regfile string) error {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("virt-win-reg", name, "--merge", regfile)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("win registry add: %w: %s", err, out)
	}
	return nil
}

func (d *DiskOperations) CopyIn(name string, file string, folder string) error {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	cmd := exec.Command("virt-copy-in", "-a", file, folder)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("win copy in: %w: %s", err, out)
	}
	return nil
} */
