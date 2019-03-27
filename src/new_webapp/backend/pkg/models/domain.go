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

// DomainOptions are the different options that a domain can have
type DomainOptions struct {
	// Viewers contains the options related with the viewers
	Viewers struct {
		// Spice contains the options related with the Spice viewer
		Spice struct {
			// Fullscreen sets if the desktop is going to be opened in
			// fullscreen when using the spice viewer
			Fullscreen bool
		}
	}
}
