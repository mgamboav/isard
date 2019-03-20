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

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/auth"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"

	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestValidate(t *testing.T) {
	assert := assert.New(t)

	t.Run("should return no error if the token is valid", func(t *testing.T) {
		cfg.Config = viper.New()
		cfg.Config.Set("tokens.secret", "godoesnotexist")

		tkn, err := auth.NewToken("egoldman")
		assert.Nil(err)
		// TODO: Improve this assert
		assert.NotNil(tkn)
	})
}

func TestString(t *testing.T) {
	assert := assert.New(t)

	t.Run("shoud return the token as a string", func(t *testing.T) {
		var tkn auth.Token = "token!"
		assert.Equal("token!", tkn.String())
	})
}
