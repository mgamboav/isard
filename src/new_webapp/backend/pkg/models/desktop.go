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

package models

import (
	"fmt"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"

	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

// Desktop is a desktop of an user
type Desktop struct {
	// ID is the unique identifier of the domain. It's formed by "_{username}_{desktopName}"
	ID string `rethinkdb:"id"`

	// Name is the name of the desktop
	Name string `rethinkdb:"name"`

	// Description is the user description of the desktop
	Description string `rethinkdb:"description"`

	// Status is the current status of the desktop
	Status string `rethinkdb:"status"`

	// Detail shows the messages in case there's an error doing an operation with the desktop
	Detail string `rethinkdb:"detail"`

	// User is the ID of the user that owns the desktop
	User string `rethinkdb:"user"`

	// OS is the Operative System of the Desktop
	OS string `rethinkdb:"os"`

	// Options are the options of the desktop
	Options DomainOptions `rethinkdb:"options"`
}

// GetUserDesktops returns all the desktops of an user
func GetUserDesktops(id string) ([]*Desktop, error) {
	res, err := r.Table("domains").GetAllByIndex("user", id).Filter(
		r.Row.Field("kind").Eq("desktop"),
	).Run(db.Session)
	if err != nil {
		return []*Desktop{}, fmt.Errorf("error querying the DB: %v", err)
	}
	defer res.Close()

	var desktops []*Desktop
	var desktop Desktop
	for res.Next(&desktop) {
		d := desktop
		desktops = append(desktops, &d)
	}

	if res.Err() != nil {
		return []*Desktop{}, fmt.Errorf("error getting the desktops from the DB: %v", res.Err())
	}

	return desktops, nil
}
