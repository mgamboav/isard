package hyper_test

import (
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"libvirt.org/libvirt-go"
)

func TestResume(t *testing.T) {
	require := require.New(t)
	assert := assert.New(t)

	cases := map[string]struct {
		PrepareDesktop func(h *hyper.Hyper) *libvirt.Domain
		ExpectedErr    string
	}{
		"resume the desktop correctly": {
			PrepareDesktop: func(h *hyper.Hyper) *libvirt.Domain {
				desktop, err := h.Start(hyper.TestMinDesktopXML(t), &hyper.StartOptions{})
				require.NoError(err)

				err = h.Suspend(desktop)
				require.NoError(err)

				return desktop
			},
		},
		"should return an error if there's an error resuming the desktop": {
			PrepareDesktop: func(h *hyper.Hyper) *libvirt.Domain {
				return &libvirt.Domain{}
			},
			ExpectedErr: "virError(Code=7, Domain=6, Message='invalid domain pointer in virDomainResume')",
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

			err = h.Resume(desktop)

			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}
		})
	}
}