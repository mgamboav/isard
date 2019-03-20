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

package auth

import (
	"errors"
	"fmt"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/db"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"
	"golang.org/x/crypto/bcrypt"

	r "gopkg.in/rethinkdb/rethinkdb-go.v5"
)

// LoginLocal logs in the user using the local database and returns the token
func LoginLocal(id, pwd string) (Token, error) {
	res, err := r.Table("users").Get(id).Run(db.Session)
	if err != nil {
		return "", fmt.Errorf("error querying the DB: %v", err)
	}

	var usr models.User
	err = res.One(&usr)
	if err != nil {
		if err == r.ErrEmptyResult {
			return "", fmt.Errorf("user not found")
		}

		return "", fmt.Errorf("error getting the user from the DB: %v", err)
	}

	if usr.Type != "local" {
		return "", fmt.Errorf("invalid authentication method: user auth type is %v", usr.Type)
	}

	err = bcrypt.CompareHashAndPassword([]byte(usr.Password), []byte(pwd))
	if err != nil {
		if err == bcrypt.ErrMismatchedHashAndPassword {
			return "", errors.New("incorrect password")
		}

		return "", fmt.Errorf("password error: %v", err)
	}

	tkn, err := NewToken(usr.ID)
	if err != nil {
		return "", fmt.Errorf("error generating the login token: %v", err)
	}

	return tkn, nil
}
