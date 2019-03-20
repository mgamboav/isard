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
	Role Role `rethinkdb:"role,reference" rethinkdb_ref:"id"`

	// Category is the category of the user
	Category Category `rethinkdb:"role,reference" rethinkdb_ref:"id"`

	// Group is the the group of the user
	Group Group `rethinkdb:"role,reference" rethinkdb_ref:"id"`

	// Quota is the quota that the user has
	Quota Quota `rethinkdb:"quota"`
}
