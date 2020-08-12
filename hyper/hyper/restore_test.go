package hyper_test

import (
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRestore(t *testing.T) {
	require := require.New(t)
	assert := assert.New(t)

	cases := map[string]struct {
		PrepareDesktop func(h *hyper.Hyper) string
		ExpectedErr    string
	}{
		"restore the desktop correctly": {
			PrepareDesktop: func(h *hyper.Hyper) string {
				desktop, err := h.Start(hyper.TestMinDesktopXML(t), &hyper.StartOptions{})
				require.NoError(err)

				err = h.Save(desktop, "test.dump")
				require.NoError(err)

				return "test.dump"
			},
		},
		"should return an error if there's an error restoring the desktop": {
			PrepareDesktop: func(h *hyper.Hyper) string {
				return ""
			},
			ExpectedErr: "virError(Code=38, Domain=12, Message='incomplete save header in '/home/darta/github/nouisard/hyper/hyper/': Is a directory')",
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			h, err := hyper.New(nil, hyper.TestLibvirtDriver(t))
			require.NoError(err)

			defer h.Close()

			path := tc.PrepareDesktop(h)

			err = h.Restore(path)

			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}
		})
	}
}
