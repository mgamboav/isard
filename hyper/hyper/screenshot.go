package hyper

import (
	"errors"
	"fmt"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) DesktopScreenshot(id string) (stream libvirt.Stream, mime string, error) {
	desktop, err := h.conn.LookupDomainByName(id)
	if err != nil {
		var e libvirt.Error
		if errors.As(err, &e) {
			switch e.Code {
			case libvirt.ERR_NO_DOMAIN:
				return "", "", ErrDesktopNotStarted

			default:
				return "", "", fmt.Errorf("desktop screenshot: %s", e.Message)
			}
		}

		return "", "", fmt.Errorf("desktops screenshot: %w", err)
	}
	defer desktop.Free()

	stream := &libvirt.Stream{}
	//The screen ID is the sequential number of screen. In case of multiple graphics cards,
	//heads are enumerated before devices, e.g. having two graphics cards,
	//both with four heads, screen ID 5 addresses the second head on the second card.
	mime, err := desktop.Screenshot(stream, 1, 0)
	if err != nil {
		return "", "", fmt.Errorf("desktop screenshot: %w", err)
	}
	return stream, mime, nil
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
