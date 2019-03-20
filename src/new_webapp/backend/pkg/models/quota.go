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

// Quota is the quota that an entity has
type Quota struct {
	// Domains contains the quota settings related with the number of domains
	Domains struct {
		// Desktops is the maximum number of desktops that an entity can have
		Desktops int `rethinkdb:"desktops"`

		// DesktopsDiskMax is the maximum size that the disk of a desktop can have (in KB)
		DesktopsDiskMax int `rethinkdb:"desktops_disk_max"`

		// Templates is the maximum number of templates that an entitty can have
		Templates int `rethinkdb:"templates"`

		// TemplatesDiskMax is the maximum size that the disk of a template can have (in KB)
		TemplatesDiskMax int `rethinkdb:"templates_disk_max"`

		// Running is the maximum number of simultaneous running desktops that the entity can have
		Running int `rethinkdb:"running"`

		// Media is the maximum number of media (isos/floppies) that the entity can have
		Media int `rethinkdb:"isos"`

		// MediaDiskMax is the maximum size that a media disk can have (in KB)
		MediaDiskMax int `rethinkdb:"isos_disk_max"`
	} `rethinkdb:"domains"`

	// Hardware contains the quota settings related with the hardware capabilites of the VMs
	Hardware struct {
		// VCPUs is the maximum number of virtual CPUs that a domain can have
		VCPUs int `rethinkdb:"vcpus"`

		// Memory is the maximum RAM that a domain can have (in KB)
		Memory int `rethinkdb:"memory"`
	}
}
