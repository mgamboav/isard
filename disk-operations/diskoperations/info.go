package diskoperations

import (
	"encoding/json"
	"errors"
	"fmt"
	"os/exec"

	"github.com/spf13/afero"
)

func (d *DiskOperations) InfoQcow2(name string) (*ImageInfoQcow2, error) {
	if _, err := d.env.FS.Stat(name); errors.Is(err, afero.ErrFileNotFound) {
		return &ImageInfoQcow2{}, ErrFileNotFound
	}

	cmd := exec.Command("qemu-img", "info", "--output", "json", name)
	out := ""
	if out, err := cmd.CombinedOutput(); err != nil {
		return &ImageInfoQcow2{}, fmt.Errorf("info: %w: %s", err, out)
	}
	//qemu-img: Could not open '/isard/PackeTracer.qcow2': Could not open '/isard/templates/_PackeTracer.qcow2': No such file or directory

	info := &ImageInfoQcow2{}

	err := json.Unmarshal([]byte(out), info)
	if err != nil {
		return &ImageInfoQcow2{}, fmt.Errorf("info: %w: %s", err, out)
	}
	return info, nil
}

/* [
    {
        "virtual-size": 48318382080,
        "filename": "Cisco.qcow2",
        "cluster-size": 4096,
        "format": "qcow2",
        "actual-size": 4169547776,
        "format-specific": {
            "type": "qcow2",
            "data": {
                "compat": "1.1",
                "lazy-refcounts": false,
                "refcount-bits": 16,
                "corrupt": false
            }
        },
        "full-backing-filename": "/isard/templates/inf/inf/rbotey/ApuntsCisco_i_PackeTracer.qcow2",
        "backing-filename": "/isard/templates/inf/inf/rbotey/ApuntsCisco_i_PackeTracer.qcow2",
        "dirty-flag": false
    },
    {
        "virtual-size": 48318382080,
        "filename": "/isard/templates/inf/inf/rbotey/ApuntsCisco_i_PackeTracer.qcow2",
        "cluster-size": 4096,
        "format": "qcow2",
        "actual-size": 2500501504,
        "format-specific": {
            "type": "qcow2",
            "data": {
                "compat": "1.1",
                "lazy-refcounts": false,
                "refcount-bits": 16,
                "corrupt": false
            }
        },
        "full-backing-filename": "/isard/templates/inf/inf/jgimenez/Template_Doc-CISCO.qcow2",
        "backing-filename": "/isard/templates/inf/inf/jgimenez/Template_Doc-CISCO.qcow2",
        "dirty-flag": false
    },
    {
        "virtual-size": 48318382080,
        "filename": "/isard/templates/inf/inf/jgimenez/Template_Doc-CISCO.qcow2",
        "cluster-size": 4096,
        "format": "qcow2",
        "actual-size": 3589496832,
        "format-specific": {
            "type": "qcow2",
            "data": {
                "compat": "1.1",
                "lazy-refcounts": false,
                "refcount-bits": 16,
                "corrupt": false
            }
        },
        "full-backing-filename": "/vimet/bases/fedora_23.qcow2",
        "backing-filename": "/vimet/bases/fedora_23.qcow2",
        "dirty-flag": false
    },
    {
        "virtual-size": 48318382080,
        "filename": "/vimet/bases/fedora_23.qcow2",
        "cluster-size": 4096,
        "format": "qcow2",
        "actual-size": 8607125504,
        "format-specific": {
            "type": "qcow2",
            "data": {
                "compat": "1.1",
                "lazy-refcounts": false,
                "refcount-bits": 16,
                "corrupt": false
            }
        },
        "dirty-flag": false
    }
] */
