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

// Role is a user role
type Role struct {
	// ID is the unique identifier of the role
	ID string `rethinkdb:"id"`

	// Name is the name of the role
	Name string `rethinkdb:"name"`

	// Description is a small description of the role
	Description string `rethinkdb:"description"`

	// TODO: this v
	// Permissions

	// Quota is the default quota of the role
	Quota Quota `rethinkdb:"quota"`
}
