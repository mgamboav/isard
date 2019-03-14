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

package log

import (
	"os"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"

	jww "github.com/spf13/jwalterweatherman"
)

// Init initializes the logging
func Init() {
	var threshold jww.Threshold

	level := cfg.Config.GetString("log.level")
	switch level {

	case "trace":
		threshold = jww.LevelTrace

	case "debug":
		threshold = jww.LevelDebug

	case "info":
		threshold = jww.LevelInfo

	case "error":
		threshold = jww.LevelError

	case "critical":
		threshold = jww.LevelCritical

	case "fatal":
		threshold = jww.LevelFatal

	default:
		threshold = jww.LevelWarn
	}

	jww.SetLogThreshold(threshold)

	f, err := os.OpenFile(cfg.Config.GetString("log.file"), os.O_RDWR|os.O_CREATE, 0644)
	if err != nil {
		jww.FATAL.Printf("error opening the log file: %v", err)
		os.Exit(1)
	}

	jww.SetLogOutput(f)
}
