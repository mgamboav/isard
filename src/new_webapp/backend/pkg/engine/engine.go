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

package engine

import (
	"fmt"
	"os"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/proto/third_party/engine/desktop"

	jww "github.com/spf13/jwalterweatherman"
	"google.golang.org/grpc"
)

// Cli is the active connection with the engine
var Cli *Client

// Client is the responsible of communicating with the engine
type Client struct {
	Desktop desktop.DesktopClient
}

// Init initializes the engine client
func Init() {
	conn, err := grpc.Dial(fmt.Sprintf("%s:%d", cfg.Config.GetString("engine.host"), cfg.Config.GetInt("engine.port")), grpc.WithInsecure())
	if err != nil {
		jww.FATAL.Printf("error connecting to the engine: %v", err)
		os.Exit(1)
	}

	Cli = &Client{}
	Cli.Desktop = desktop.NewDesktopClient(conn)
}
