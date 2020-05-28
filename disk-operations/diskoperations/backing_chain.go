package diskoperations

import (
	"encoding/json"
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

func (d *DiskOperations) BackingChainQcow2(name string) ([]string, error) {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return []string{}, ErrBackingFileNotFound
	}

	cmd := exec.Command("qemu-img", "info", "--backing-chain", "--output", "json", name)
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
