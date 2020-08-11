package hyper_test

import (
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"libvirt.org/libvirt-go"
)

func TestGet(t *testing.T) {
	require := require.New(t)
	assert := assert.New(t)

	cases := map[string]struct {
		Name          string
		PrepareTest   func(h *hyper.Hyper)
		ExpectedErr   string
		ExpectedState libvirt.DomainState
	}{
		"should get the desktop correctly": {
			Name:          "test",
			ExpectedState: libvirt.DOMAIN_RUNNING,
		},
		"should return ErrDesktopNotFound if the desktop doesn't exist": {
			ExpectedErr: hyper.ErrDesktopNotFound.Error(),
		},
		"should return an error if there's an error getting the desktop": {
			Name: "test",
			PrepareTest: func(h *hyper.Hyper) {
				h.Close()
			},
			ExpectedErr: "virError(Code=6, Domain=20, Message='invalid connection pointer in virDomainLookupByName')",
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			h, err := hyper.New(nil, hyper.TestLibvirtDriver(t))
			require.NoError(err)

			defer h.Close()

			if tc.PrepareTest != nil {
				tc.PrepareTest(h)
			}

			desktop, err := h.Get(tc.Name)
			if desktop != nil {
				defer desktop.Free()

				state, _, err := desktop.GetState()
				assert.NoError(err)
				assert.Equal(tc.ExpectedState, state)

			} else {
				if tc.ExpectedState != 0 {
					t.Errorf("expecting desktop state '%v' but the desktop is nil", tc.ExpectedState)
				}
			}

			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}
		})
	}
}
