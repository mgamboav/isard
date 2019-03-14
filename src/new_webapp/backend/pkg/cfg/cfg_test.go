/*
 * Copyright (C) 2019 IsardVDI
 * Authors: IsardVDI Authors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package cfg_test

import (
	"io/ioutil"
	"os"
	"testing"
	"time"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/utils/tests"

	"github.com/stretchr/testify/assert"
)

func TestInit(t *testing.T) {
	assert := assert.New(t)

	t.Run("should initialize the configuration correctly", func(t *testing.T) {
		err := ioutil.WriteFile("config.toml", []byte(""), 0644)
		assert.Nil(err)

		cfg.Init()
		assert.Equal("localhost", cfg.Config.GetString("db.host"))

		err = os.Remove("config.toml")
		assert.Nil(err)
	})

	t.Run("should exit if there's an error intializing the configuration", func(t *testing.T) {
		tests.AssertExits(t, cfg.Init)
	})

	t.Run("should reload correctly the configuration", func(t *testing.T) {
		err := ioutil.WriteFile("config.toml", []byte(""), 0644)
		assert.Nil(err)

		cfg.Init()
		assert.Equal("localhost", cfg.Config.GetString("db.host"))

		err = ioutil.WriteFile("config.toml", []byte(`[db]
host = "isard-database"`), 0644)
		assert.Nil(err)

		time.Sleep(1 * time.Second)

		assert.Equal("isard-database", cfg.Config.GetString("db.host"))

		err = os.Remove("config.toml")
		assert.Nil(err)
	})
}
