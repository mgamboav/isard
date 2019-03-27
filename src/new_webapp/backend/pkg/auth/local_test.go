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

package auth_test

import (
	"errors"
	"strings"
	"testing"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"

	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func TestLoginLocal(t *testing.T) {
	assert := assert.New(t)
	var emptyTkn auth.Token = ""

	t.Run("should return an error if there's an error getting the user", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{}, errors.New("testing error"))
		db.Session = mock

		tkn, err := auth.LoginLocal("egoldman", "")
		assert.EqualError(err, "error getting the user: error querying the DB: testing error")
		assert.Equal(emptyTkn, tkn)

		mock.AssertExpectations(t)
	})

	t.Run("should return a token if the authentication suceeds", func(t *testing.T) {
		cfg.Config = viper.New()
		cfg.SetDefaults()

		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":       "egoldman",
				"kind":     "local",
				"password": "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
			},
		}, nil)
		db.Session = mock

		tkn, err := auth.LoginLocal("egoldman", "P4$$w0rd!")
		assert.Nil(err)
		assert.Equal(3, len(strings.Split(tkn.String(), ".")))

		mock.AssertExpectations(t)
	})

	t.Run("should return an error if the user type isn't local", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":   "egoldman",
				"kind": "ldap",
			},
		}, nil)
		db.Session = mock

		tkn, err := auth.LoginLocal("egoldman", "")
		assert.EqualError(err, "invalid authentication method: user auth type is ldap")
		assert.Equal(emptyTkn, tkn)

		mock.AssertExpectations(t)
	})

	t.Run("should return an error if the password is incorrect", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":       "egoldman",
				"kind":     "local",
				"password": "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
			},
		}, nil)
		db.Session = mock

		tkn, err := auth.LoginLocal("egoldman", "n0pe!")
		assert.EqualError(err, "incorrect password")
		assert.Equal(emptyTkn, tkn)

		mock.AssertExpectations(t)
	})

	t.Run("should return an error if there's an error checking the password", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":   "egoldman",
				"kind": "local",
			},
		}, nil)
		db.Session = mock

		tkn, err := auth.LoginLocal("egoldman", "P4$$w0rd!")
		assert.EqualError(err, "password error: crypto/bcrypt: hashedSecret too short to be a bcrypted password")
		assert.Equal(emptyTkn, tkn)

		mock.AssertExpectations(t)
	})
}
