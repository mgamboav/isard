package hyper_test

import (
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"libvirt.org/libvirt-go"
)

func TestStart(t *testing.T) {
	defer hyper.TestDesktopsCleanup(t)

	require := require.New(t)
	assert := assert.New(t)

	cases := map[string]struct {
		XML             string
		Opts            *hyper.StartOptions
		RealConn        bool
		ExpectedErr     string
		ExpectedDesktop func(desktop *libvirt.Domain)
	}{
		"start the desktop correctly": {
			XML:  hyper.TestMinDesktopXML(t),
			Opts: &hyper.StartOptions{},
			ExpectedDesktop: func(desktop *libvirt.Domain) {
				state, _, err := desktop.GetState()

				assert.NoError(err)
				assert.Equal(libvirt.DOMAIN_RUNNING, state)
			},
		},
		"start the desktop paused correcly": {
			XML:      hyper.TestMinDesktopXML(t, "kvm"),
			Opts:     &hyper.StartOptions{Paused: true},
			RealConn: true,
			ExpectedDesktop: func(desktop *libvirt.Domain) {
				state, _, err := desktop.GetState()

				assert.NoError(err)
				assert.Equal(libvirt.DOMAIN_PAUSED, state)
			},
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			var conn string
			if !tc.RealConn {
				conn = hyper.TestLibvirtDriver(t)
			}

			h, err := hyper.New(nil, conn)
			require.NoError(err)

			defer h.Close()

			desktop, err := h.Start(tc.XML, tc.Opts)
			if desktop != nil {
				defer desktop.Free()
			}

			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}

			tc.ExpectedDesktop(desktop)
		})
	}
}
