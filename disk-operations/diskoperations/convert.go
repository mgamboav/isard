package diskoperations

import (
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

// TODO: Will always be qcow? or we should check filetypes before proceeding?
func (d *DiskOperations) Convert(name_input string, name_output string, format_input string, format_output string) error {
	if _, err := d.env.FS.Stat(name_input); errors.Is(err, afero.ErrFileNotFound) {
		return ErrFileNotFound
	}

	correct := false
	output := []string{"qcow2", "raw", "vmdk"}
	for _, i := range output {
		if i == format_output {
			correct = true
			break
		}
	}

	cmd := exec.Command("qemu-img", "convert", "-f", format_input, "-O", format_output, name_input, name_output)
	if out, err := cmd.CombinedOutput(); err != nil {
		return fmt.Errorf("convert image: %w: %s", err, out)
	}
	return nil
}
