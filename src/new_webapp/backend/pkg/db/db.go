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

package db

import (
	"os"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"

	jww "github.com/spf13/jwalterweatherman"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

// Session is the opened RethinkDB connection
var Session *r.Session

// Init initalizes the database connection
func Init() {
	var err error
	Session, err = r.Connect(r.ConnectOpts{
		Address:  cfg.Config.GetString("db.host"),
		Database: cfg.Config.GetString("db.name"),
	})

	if err != nil {
		jww.FATAL.Printf("error connecting to the DB: %v", err)
		os.Exit(1)
	}
}
