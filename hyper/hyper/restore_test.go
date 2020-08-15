package hyper_test

import (
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"testing"

	"github.com/isard-vdi/isard/hyper/hyper"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRestore(t *testing.T) {
	require := require.New(t)
	assert := assert.New(t)

	cases := map[string]struct {
		PrepareTest func(h *hyper.Hyper) string
		ExpectedErr string
	}{
		"restore the desktop correctly": {
			PrepareTest: func(h *hyper.Hyper) string {
				desktop, err := h.Start(hyper.TestMinDesktopXML(t), &hyper.StartOptions{})
				require.NoError(err)

				dir, err := ioutil.TempDir("", "dumps")
				if err != nil {
					log.Fatal(err)
				}

				path := filepath.Join(dir, "test.dump")
				err = h.Save(desktop, path)
				require.NoError(err)

				return path
			},
		},
		"should return an error as the libvirt conection is closed. Using tempdir": {
			PrepareTest: func(h *hyper.Hyper) string {
				h.Close()

				dir, err := ioutil.TempDir("", "dumps")
				if err != nil {
					log.Fatal(err)
				}

				path := filepath.Join(dir, "test.dump")
				ioutil.WriteFile(path, []byte("content"), os.FileMode(0777))
				return path
			},
			ExpectedErr: "virError(Code=6, Domain=20, Message='invalid connection pointer in virDomainRestore')",
		},
		"should return an error if the path is incorrect or file missing": {
			PrepareTest: func(h *hyper.Hyper) string {
				return ""
			},
			ExpectedErr: "stat : no such file or directory",
		},
	}

	for name, tc := range cases {
		t.Run(name, func(t *testing.T) {
			h, err := hyper.New(nil, hyper.TestLibvirtDriver(t))
			require.NoError(err)

			defer h.Close()

			path := tc.PrepareTest(h)

			err = h.Restore(path)

			if tc.ExpectedErr == "" {
				assert.NoError(err)
			} else {
				assert.EqualError(err, tc.ExpectedErr)
			}
			os.RemoveAll(path)
		})
	}
}
