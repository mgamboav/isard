package hyper

import (
	"errors"
	"fmt"
	"os"
	"os/exec"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) QMPScreenshot(name string) (image *os.File, error) {
	cmdtxt := "{'execute':'screendump', 'arguments':{'filename':'/tmp/image.ppm'}}"
	cmd := exec.Command("virsh", "qemu-monitor-command", name, cmdtxt)
	if out, err := cmd.CombinedOutput(); err != nil {
		return os.File, fmt.Errorf("screenshot: %w: %s", err, out)
	}
	return os.File, err
}



/* cmd='{"execute":"screendump", "arguments":{"filename":"/tmp/%s.ppm"}}' % domain
cmd='{"execute":"system_powerdown"}'
cmd='{"execute":"send-key", "arguments": {"keys":["ctrl","alt","delete"]}}'
cmd='{ "execute": "balloon", "arguments": { "value": 536870912 } }'
cmd='{ "execute": "block_set_io_throttle", "arguments": { "device": "virtio0", \
								   "bps": "1000000",    \
								   "bps_rd": "0",       \
								   "bps_wr": "0",       \
								   "iops": "0",         \
								   "iops_rd": "0",      \
								   "iops_wr": "0" } }'
cmd='{ "execute": "set_password", "arguments": { "protocol": "vnc", \
								   "password": "secret" } }'
cmd='{ "execute": "expire_password", "arguments": { "protocol": "vnc", \
									  "time": "+60" } }'
 */