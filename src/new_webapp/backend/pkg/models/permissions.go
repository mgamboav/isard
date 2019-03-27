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

// Permissions are the permissions of a resource
type Permissions struct {
	// Public sets if the resource is public or not
	Public bool

	// Roles are the roles that have access to the resource
	Roles []string

	// Categories are the categories that have acess to the resource
	Categories []string

	// Groups are the groups that have access to the resource
	Groups []string

	// Users are the users that have access to the resource
	Users []string
}
