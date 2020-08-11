package hyper_test

import (
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestList(t *testing.T) {
	require := require.New(t)
	assert := assert.New(t)

	cases := map[string]struct {
		DesktopNames []string
		ExpectedErr  string
	}{
		"should list the desktops correctly": {
			DesktopNames: []string{"test"},
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			h, err := hyper.New(nil, hyper.TestLibvirtDriver(t))
			require.NoError(err)

			defer h.Close()

			desktops, err := h.List()

			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}

			names := []string{}
			for _, desktop := range desktops {
				name, err := desktop.GetName()
				assert.NoError(err)

				names = append(names, name)
			}

			assert.Equal(tc.DesktopNames, names)
		})
	}
}
