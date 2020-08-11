package hyper

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"strings"
	"testing"

	"libvirt.org/libvirt-go"
)

func TestLibvirtDriver(t *testing.T) string {
	xmlPath, err := filepath.Abs("testdata/test_default_conn.xml")
	if err != nil {
		t.Errorf("get xml path: %v", err)
		return ""
	}

	return fmt.Sprintf("test://%s", xmlPath)
}

func TestMinDesktopXML(t *testing.T, domTypes ...string) string {
	var domType string
	if len(domTypes) == 0 {
		domType = "test"
	} else {
		domType = domTypes[0]
	}

	minDesktop, err := ioutil.ReadFile("testdata/min_desktop.xml")
	if err != nil {
		t.Errorf("get minimum domain XML definition: %v", err)
		return ""
	}

	return fmt.Sprintf(string(minDesktop), domType)
}

func TestDesktopsCleanup(t *testing.T) {
	conn, err := libvirt.NewConnect("qemu:///system")
	if err != nil {
		t.Errorf("connect to libvirt: %v", err)
		return
	}

	desktops, err := conn.ListAllDomains(libvirt.CONNECT_LIST_DOMAINS_ACTIVE | libvirt.CONNECT_LIST_DOMAINS_INACTIVE)
	if err != nil {
		t.Errorf("list all domains: %v", err)
		return
	}

	for _, desktop := range desktops {
		name, err := desktop.GetName()
		if err != nil {
			t.Errorf("get desktop name: %v", err)
			return
		}

		if strings.HasPrefix(name, "isard-test-") {
			if err := desktop.Destroy(); err != nil {
				t.Errorf("destroy desktop: %v", err)
				return
			}
		}
	}
}
