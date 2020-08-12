package hyper_test

import (
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
)

func TestHyperNew(t *testing.T) {
	assert := assert.New(t)

	cases := map[string]struct {
		URI           string
		ExpectedError string
	}{
		"should create the hypervisor correctly": {},
		"should return an error if there's an error connecting to the libvirt daemon": {
			URI:           ":::://///",
			ExpectedError: "connect to libvirt: virError(Code=1, Domain=45, Message='internal error: Unable to parse URI :::://///')",
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			h, err := hyper.New(nil, tc.URI)
			if h != nil {
				defer h.Close()
			}

			if tc.ExpectedError == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedError)
			}
		})
	}
}
