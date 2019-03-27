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

package models_test

import (
	"errors"
	"testing"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"

	"github.com/stretchr/testify/assert"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func TestGetUserDesktops(t *testing.T) {
	assert := assert.New(t)
	emptyDesktops := []*models.Desktop{}

	t.Run("should return the desktops correctly", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").GetAllByIndex("user", "nefix").Filter(
			r.Row.Field("kind").Eq("desktop"),
		)).Return([]interface{}{
			map[string]interface{}{
				"id":          "_nefix_Debian",
				"name":        "Debian",
				"description": "This is a Debian desktop",
				"status":      "Stopped",
				"detail":      "everything works",
				"user":        "nefix",
				"os":          "linux",
				"options": map[string]interface{}{
					"viewers": map[string]interface{}{
						"spice": map[string]interface{}{
							"fullscreen": true,
						},
					},
				},
			},
			map[string]interface{}{
				"id":          "_nefix_NixOS",
				"name":        "NixOS",
				"description": "This is a NixOS desktop",
				"status":      "Failed",
				"detail":      "no space left in the disk",
				"user":        "nefix",
				"os":          "linux",
			},
		}, nil)
		db.Session = mock

		expectedDesktops := []*models.Desktop{
			&models.Desktop{
				ID:          "_nefix_Debian",
				Name:        "Debian",
				Description: "This is a Debian desktop",
				Status:      "Stopped",
				Detail:      "everything works",
				User:        "nefix",
				OS:          "linux",
				Options:     models.DomainOptions{},
			},
			&models.Desktop{
				ID:          "_nefix_NixOS",
				Name:        "NixOS",
				Description: "This is a NixOS desktop",
				Status:      "Failed",
				Detail:      "no space left in the disk",
				User:        "nefix",
				OS:          "linux",
			},
		}
		expectedDesktops[0].Options.Viewers.Spice.Fullscreen = true

		d, err := models.GetUserDesktops("nefix")

		assert.Nil(err)
		assert.Equal(expectedDesktops, d)
	})

	t.Run("should return an error if there's an error querying the DB", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").GetAllByIndex("user", "nefix").Filter(
			r.Row.Field("kind").Eq("desktop"),
		)).Return([]interface{}{}, errors.New("testing error"))
		db.Session = mock

		d, err := models.GetUserDesktops("nefix")

		assert.EqualError(err, "error querying the DB: testing error")
		assert.Equal(emptyDesktops, d)
	})

	t.Run("should return an error if there's an error unmarshaling the db response", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("domains").GetAllByIndex("user", "nefix").Filter(
			r.Row.Field("kind").Eq("desktop"),
		)).Return([]interface{}{
			0,
		}, nil)
		db.Session = mock

		d, err := models.GetUserDesktops("nefix")

		assert.EqualError(err, "error getting the desktops from the DB: rethinkdb: could not decode type int into Go value of type models.Desktop")
		assert.Equal(emptyDesktops, d)
	})
}
