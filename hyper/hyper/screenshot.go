package hyper

import (
	"errors"
	"fmt"
	"os"
	"os/exec"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) DesktopScreenshot(id string) (image string, error) {
	desktop, err := h.conn.LookupDomainByName(id)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return ErrDesktopNotStarted

			default:
				return fmt.Errorf("desktop screenshot: %s", e.Message)
			}
		}

		return fmt.Errorf("desktops screenshot: %w", err)
	}
	defer desktop.Free()

	screen, err := desktop.Screenshot(&libvirt.Stream{},1)
	if err != nil {
		return "", fmt.Errorf("desktop screenshot: %w", err)
	}
	return screen, nil
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