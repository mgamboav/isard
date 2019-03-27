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

	"github.com/dgrijalva/jwt-go"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"

	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestNewToken(t *testing.T) {
	assert := assert.New(t)

	t.Run("should return a new token", func(t *testing.T) {
		cfg.Config = viper.New()
		cfg.Config.Set("tokens.secret", "godoesnotexist")

		tkn, err := auth.NewToken("egoldman")
		assert.Nil(err)
		// TODO: Improve this assert
		assert.NotNil(tkn)
	})
}

func TestValidate(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.SetDefaults()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	t.Run("should return true if the token is valid", func(t *testing.T) {
		tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
			Usr: "nefix",
			StandardClaims: jwt.StandardClaims{
				ExpiresAt: time.Now().Add(
					5 * time.Minute,
				).Unix(),
			},
		}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
		assert.Nil(err)
		var tkn = auth.Token(tknStr)

		assert.True(tkn.Validate())
	})

	t.Run("should return true if there's an error parsing the token", func(t *testing.T) {
		var tkn auth.Token = "invalid!"
		assert.False(tkn.Validate())
	})

	t.Run("should return false if the token isn't valid (for example, has already expired)", func(t *testing.T) {
		tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
			Usr: "nefix",
			StandardClaims: jwt.StandardClaims{
				ExpiresAt: time.Now().Add(
					-5 * time.Minute,
				).Unix(),
			},
		}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
		assert.Nil(err)
		var tkn = auth.Token(tknStr)

		assert.False(tkn.Validate())
	})
}

func TestRenew(t *testing.T) {
	assert := assert.New(t)
	cfg.Config = viper.New()
	cfg.SetDefaults()
	cfg.Config.Set("tokens.secret", "Ⓐ")

	t.Run("should renew the token correctly", func(t *testing.T) {
		originalExpirationTime := time.Now().Add(1 * time.Minute)
		tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
			Usr: "nefix",
			StandardClaims: jwt.StandardClaims{
				ExpiresAt: originalExpirationTime.Unix(),
			},
		}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
		assert.Nil(err)
		var tkn = auth.Token(tknStr)

		assert.Nil(tkn.Renew())

		claims := &auth.TokenClaims{}
		parsedTkn, err := jwt.ParseWithClaims(tkn.String(), claims, func(token *jwt.Token) (interface{}, error) {
			return []byte(cfg.Config.GetString("tokens.secret")), nil
		})
		assert.Nil(err)
		assert.True(parsedTkn.Valid)

		newExpirationTime := time.Unix(claims.ExpiresAt, 0)

		assert.True(newExpirationTime.After(originalExpirationTime))
	})

	t.Run("should return an error if there's an error parsing the token", func(t *testing.T) {
		var invalidTkn auth.Token = "invalid!"
		err := invalidTkn.Renew()
		assert.EqualError(err, "error renewing the token: the token is invalid or has already expired")
	})

	t.Run("should return an error if the token is invalid", func(t *testing.T) {
		tknStr, err := jwt.NewWithClaims(jwt.SigningMethodHS512, &auth.TokenClaims{
			Usr: "nefix",
			StandardClaims: jwt.StandardClaims{
				ExpiresAt: time.Now().Add(
					-5 * time.Minute,
				).Unix(),
			},
		}).SignedString([]byte(cfg.Config.GetString("tokens.secret")))
		assert.Nil(err)
		var invalidTkn = auth.Token(tknStr)

		err = invalidTkn.Renew()
		assert.EqualError(err, "error renewing the token: the token is invalid or has already expired")
	})
}

func TestString(t *testing.T) {
	assert := assert.New(t)

	t.Run("shoud return the token as a string", func(t *testing.T) {
		var tkn auth.Token = "token!"
		assert.Equal("token!", tkn.String())
	})
}
