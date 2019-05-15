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

package engine_test

import (
	"testing"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/engine"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/utils/tests"

	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestInit(t *testing.T) {
	assert := assert.New(t)

	t.Run("should initialize the client if everything works as expected", func(t *testing.T) {
		port, err := tests.GetFreePort()
		assert.Nil(err)

		cfg.Config = viper.New()
		cfg.SetDefaults()
		cfg.Config.Set("engine.port", port)

		engine.Init()

		assert.NotNil(engine.Cli.Desktop)
	})

	t.Run("should exit if there's an error initializing the engine client", func(t *testing.T) {
		tests.AssertExits(t, engine.Init)
	})
}
