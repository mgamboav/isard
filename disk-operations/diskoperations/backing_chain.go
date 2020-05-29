package diskoperations

import (
	"encoding/json"
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

func (d *DiskOperations) BackingChainQcow2(path string) ([]string, error) {
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return []string{}, ErrBackingFileNotFound
	}

	cmd := exec.Command("qemu-img", "info", "--backing-chain", "--output", "json", path)
	out := ""
	if out, err := cmd.CombinedOutput(); err != nil {
		return []string{}, fmt.Errorf("backing chain: %w: %s", err, out)
	}
	//qemu-img: Could not open '/isard/PackeTracer.qcow2': Could not open '/isard/templates/_PackeTracer.qcow2': No such file or directory
	info := []ImageInfoQcow2{}

	err := json.Unmarshal([]byte(out), info)
	if err != nil {
		return []string{}, fmt.Errorf("info: %w: %s", err, out)
	}

	bc := []string{}
	for _, i := range info {
		bc = append(bc, i.BackingFilename)
	}
	return bc, nil
}

// This only modifies backing file pointer in path
func (d *DiskOperations) BackingChainQcow2Replace(path string, backingpath string) error {
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	if _, err := d.env.FS.Stat(backingpath); errors.Is(err, afero.ErrFileNotFound) {
		return ErrBackingFileNotFound
	}

	cmd := exec.Command("qemu-img", "rebase", "-f", "-u", "-b", backingpath, path)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("rebase image: %w: %s", err, out)
	}
	return nil
}

// This will commit all changes between backing and path to path
// So path is the only file that will be modified.
func (d *DiskOperations) BackingChainQcow2Rebase(path string, backingpath string, delete_intermediates bool) error {
	// TODO: Should we add a parameter to delete intermediate files in chain between path and backing?
	// Be sure the intermediates are not being used by any other derived file!
	if _, err := d.env.FS.Stat(path); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	if _, err := d.env.FS.Stat(backingpath); errors.Is(err, afero.ErrFileNotFound) {
		return ErrBackingFileNotFound
	}

	cmd := exec.Command("qemu-img", "rebase", "-f", "-b", backingpath, path)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("rebase image: %w: %s", err, out)
	}
	return nil
}
