package hyper_test

import (
	"io/ioutil"
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"libvirt.org/libvirt-go"
)

func TestXMLGet(t *testing.T) {
	require := require.New(t)
	assert := assert.New(t)

	okCaseXML, err := ioutil.ReadFile("testdata/xml_test-should_return_the_XML_correctly.xml")
	require.NoError(err)

	cases := map[string]struct {
		PrepareDesktop func(h *hyper.Hyper) *libvirt.Domain
		ExpectedXML    string
		ExpectedErr    string
	}{
		"should return the XML correctly": {
			PrepareDesktop: func(h *hyper.Hyper) *libvirt.Domain {
				desktop, err := h.Get("test")
				require.NoError(err)

				return desktop
			},
			ExpectedXML: string(okCaseXML),
		},
		"should return an error if there's an error getting the XML": {
			PrepareDesktop: func(h *hyper.Hyper) *libvirt.Domain {
				return &libvirt.Domain{}
			},
			ExpectedErr: "virError(Code=7, Domain=6, Message='invalid domain pointer in virDomainGetXMLDesc')",
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			h, err := hyper.New(nil, hyper.TestLibvirtDriver(t))
			require.NoError(err)

			defer h.Close()

			desktop := tc.PrepareDesktop(h)
			if desktop != nil {
				defer desktop.Free()
			}

			xml, err := h.XMLGet(desktop)
			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}

			assert.Equal(tc.ExpectedXML, xml)
		})
	}
}
