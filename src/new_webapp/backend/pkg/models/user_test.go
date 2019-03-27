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

func TestGetUser(t *testing.T) {
	assert := assert.New(t)
	var emptyUsr = &models.User{}

	t.Run("should return the user", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":       "egoldman",
				"kind":     "local",
				"active":   true,
				"password": "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
				"name":     "Emma Goldman",
				"mail":     "egoldman@example.org",
				"role":     "admin",
				"category": "admin",
				"group":    "admin",
				"quota": map[string]interface{}{
					"domains": map[string]interface{}{
						"desktops":           99,
						"desktops_disk_max":  999999999,
						"isos":               99,
						"isos_disk_max":      999999999,
						"running":            99,
						"templates":          99,
						"templates_disk_max": 999999999,
					},
					"hardware": map[string]interface{}{
						"memory": 20000000,
						"vcpus":  8,
					},
				},
			},
		}, nil)
		db.Session = mock

		expectedUsr := &models.User{
			ID:       "egoldman",
			Type:     "local",
			Password: "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
			Name:     "Emma Goldman",
			Mail:     "egoldman@example.org",
			Role:     "admin",
			Category: "admin",
			Group:    "admin",
			Quota:    models.Quota{},
		}
		expectedUsr.Quota.Domains.Desktops = 99
		expectedUsr.Quota.Domains.DesktopsDiskMax = 999999999
		expectedUsr.Quota.Domains.Media = 99
		expectedUsr.Quota.Domains.MediaDiskMax = 999999999
		expectedUsr.Quota.Domains.Running = 99
		expectedUsr.Quota.Domains.Templates = 99
		expectedUsr.Quota.Domains.TemplatesDiskMax = 999999999
		expectedUsr.Quota.Hardware.VCPUs = 8
		expectedUsr.Quota.Hardware.Memory = 20000000

		usr, err := models.GetUser("egoldman")
		assert.Nil(err)
		assert.Equal(expectedUsr, usr)
	})

	t.Run("should return an error if there's an error querying the DB", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{}, errors.New("testing error"))
		db.Session = mock

		usr, err := models.GetUser("egoldman")
		assert.EqualError(err, "error querying the DB: testing error")
		assert.Equal(emptyUsr, usr)

		mock.AssertExpectations(t)
	})

	t.Run("should return an error if the user isn't found", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{}, nil)
		db.Session = mock

		usr, err := models.GetUser("egoldman")
		assert.EqualError(err, "user not found")
		assert.Equal(emptyUsr, usr)

		mock.AssertExpectations(t)
	})

	t.Run("should return an error if there's an error getting the user from the DB", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			0,
		}, nil)
		db.Session = mock

		usr, err := models.GetUser("egoldman")
		assert.EqualError(err, "error getting the user from the DB: rethinkdb: could not decode type int into Go value of type models.User")
		assert.Equal(emptyUsr, usr)

		mock.AssertExpectations(t)
	})
}
