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

package cfg

import (
	"os"

	"github.com/fsnotify/fsnotify"
	jww "github.com/spf13/jwalterweatherman"
	"github.com/spf13/viper"
)

// Config is the variable that contains the configuration
var Config *viper.Viper

// Init prepares the configuration and reads it
func Init() {
	Config = viper.New()
	SetDefaults()

	if err := Config.ReadInConfig(); err != nil {
		jww.FATAL.Printf("error reading the configuration: %v", err)
		os.Exit(1)
	}

	Config.WatchConfig()
	Config.OnConfigChange(func(e fsnotify.Event) {
		jww.INFO.Println("configuration file changed")
	})
}

// SetDefaults sets the default configurations for Viper
func SetDefaults() {
	Config.SetConfigName("config")
	Config.AddConfigPath(".")
	Config.AddConfigPath("$HOME/.config/isard")
	Config.AddConfigPath("$HOME/.isard")
	Config.AddConfigPath("/etc/isard")

	Config.SetDefault("tokens", map[string]interface{}{
		"secret": nil,
		// Minutes
		"lifespan": 5,
	})

	Config.SetDefault("db", map[string]interface{}{
		"host": "isard-database",
		"port": 28015,
		"name": "isard",
	})

	Config.SetDefault("log", map[string]interface{}{
		"level": "warn",
		"file":  "backend.log",
	})

	Config.SetDefault("engine", map[string]interface{}{
		"host": "isard-app",
		"port": 1313,
	})
}
