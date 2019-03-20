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

// Category is a category of users
type Category struct {
	// ID is the unique identifier of the category
	ID string `rethinkdb:"id"`

	// Name is the name of the category
	Name string `rethinkdb:"name"`

	// Description is a small description of the category
	Description string `rethinkdb:"description"`

	// Role is the parent role of the category
	Role Role `rethinkdb:"role"`

	// Quota is the default quota of the category
	Quota Quota `rethinkdb:"quota"`
}
