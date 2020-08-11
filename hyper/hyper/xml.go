package hyper

import (
	"fmt"

	"libvirt.org/libvirt-go"
)

func (h *Hyper) XMLGet(desktop *libvirt.Domain) (string, error) {
	xml, err := desktop.GetXMLDesc(libvirt.DOMAIN_XML_SECURE)
	if err != nil {
		return "", fmt.Errorf("get desktop XML: %w", err)
	}

	return xml, nil
}
