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
	"testing"
	"time"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"

	"github.com/dgrijalva/jwt-go"
	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

func TestCanAccess(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
		Usr: "egoldman",
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(
				5 * time.Minute,
			).Unix(),
		},
	}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
	assert.Nil(err)
	var tkn = auth.Token(tknStr)

	t.Run("should give access to the user if it has permissions to acess it", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":       "egoldman",
				"kind":     "local",
				"role":     "user",
				"password": "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
			},
		}, nil)
		db.Session = mock

		assert.True(tkn.CanAccess("egoldman"))
	})

	t.Run("should give access if the user is an admin", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":       "egoldman",
				"kind":     "local",
				"role":     "admin",
				"password": "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
			},
		}, nil)
		db.Session = mock

		assert.True(tkn.CanAccess("nefix"))
	})

	t.Run("should deny the access if the user doesn't have permissions to access it", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{
			map[string]interface{}{
				"id":       "egoldman",
				"kind":     "local",
				"role":     "user",
				"password": "$2a$12$MqRkRgdLoKqEIM2Vbh1Xa.2ZyLQWEdk3WAYXLFKsQFchPInHzN1NC",
			},
		}, nil)
		db.Session = mock

		assert.False(tkn.CanAccess("nefix"))
	})

	t.Run("should deny the access if there's an error parsing the token", func(t *testing.T) {
		var invalidTkn auth.Token = "invalid!"
		assert.False(invalidTkn.CanAccess("nefix"))
	})

	t.Run("should deny the access if the token is invalid", func(t *testing.T) {
		tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
			Usr: "egoldman",
			StandardClaims: jwt.StandardClaims{
				ExpiresAt: time.Now().Add(
					-5 * time.Minute,
				).Unix(),
			},
		}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
		assert.Nil(err)
		var invalidTkn = auth.Token(tknStr)

		assert.False(invalidTkn.CanAccess("nefix"))
	})

	t.Run("should deny the access if there's an error getting the user in the DB", func(t *testing.T) {
		mock := r.NewMock()
		mock.On(r.Table("users").Get("egoldman")).Return([]interface{}{}, nil)
		db.Session = mock

		assert.False(tkn.CanAccess("nefix"))
	})
}
