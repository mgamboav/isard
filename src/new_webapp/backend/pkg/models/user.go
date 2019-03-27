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

// User is an individual user of Isard
type User struct {
	// ID is the unique identifier of the User (it's also the username)
	ID string `rethinkdb:"id"`

	// Type is the authentication kind
	Type string `rethinkdb:"kind"`

	// Password is the password of the user if the user authentication kind is Local. It's stored using bcrypt
	Password string `rethinkdb:"password"`

	// Name is the name of the user
	Name string `rethinkdb:"name"`

	// Mail is the mail of the user
	Mail string `rethinkdb:"mail"`

	// Role is the role of the user
	Role string `rethinkdb:"role"`

	// Category is the category of the user
	Category string `rethinkdb:"category"`

	// Group is the the group of the user
	Group string `rethinkdb:"group"`

	// Quota is the quota that the user has
	Quota Quota `rethinkdb:"quota"`
}

// GetUser returns searches an user in the DB
func GetUser(id string) (*User, error) {
	res, err := r.Table("users").Get(id).Run(db.Session)
	if err != nil {
		return &User{}, fmt.Errorf("error querying the DB: %v", err)
	}
	defer res.Close()

	var usr User
	err = res.One(&usr)
	if err != nil {
		if err == r.ErrEmptyResult {
			return &User{}, fmt.Errorf("user not found")
		}

		return &User{}, fmt.Errorf("error getting the user from the DB: %v", err)
	}

	return &usr, nil
}
