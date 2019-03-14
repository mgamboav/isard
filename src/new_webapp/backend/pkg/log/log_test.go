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

package log_test

import (
	"os"
	"testing"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/log"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/utils/tests"

	jww "github.com/spf13/jwalterweatherman"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestInit(t *testing.T) {
	assert := assert.New(t)

	t.Run("should initialize the logging correctly", func(t *testing.T) {
		cfg.Config = viper.New()
		cfg.SetDefaults()

		levels := map[string]jww.Threshold{
			"trace":    jww.LevelTrace,
			"debug":    jww.LevelDebug,
			"info":     jww.LevelInfo,
			"warn":     jww.LevelWarn,
			"error":    jww.LevelError,
			"critical": jww.LevelCritical,
			"fatal":    jww.LevelFatal,
		}

		for level, threshold := range levels {
			cfg.Config.Set("log.level", level)
			log.Init()
			assert.Equal(threshold, jww.GetLogThreshold())
		}

		jww.FATAL.Println("muerte al estado y vivan mis amigas")
		assert.FileExists("backend.log")

		assert.Nil(os.Remove("backend.log"))
	})

	t.Run("should exit if there's an error opening the log file", func(t *testing.T) {
		cfg.Config = viper.New()
		cfg.SetDefaults()
		cfg.Config.Set("log.file", "")

		tests.AssertExits(t, log.Init)
	})
}
