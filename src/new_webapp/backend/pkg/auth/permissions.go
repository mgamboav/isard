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
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"

	"github.com/dgrijalva/jwt-go"
)

// CanAccess checks if an user can access to a specific resource
func (t Token) CanAccess(ownerID string) bool {
	claims := &TokenClaims{}

	tkn, err := jwt.ParseWithClaims(t.String(), claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(cfg.Config.GetString("tokens.secret")), nil
	})
	if err != nil || !tkn.Valid {
		return false
	}

	usr, err := models.GetUser(claims.Usr)
	if err != nil {
		return false
	}

	if usr.Role == "admin" {
		return true
	}

	if usr.ID == ownerID {
		return true
	}

	return false
}
