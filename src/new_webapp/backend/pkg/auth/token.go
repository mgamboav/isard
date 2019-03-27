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
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/cfg"
)

// Token is a JWT token
type Token string

// TokenClaims are going to be embedded inside the JWT Token
type TokenClaims struct {
	Usr string
	jwt.StandardClaims
}

// NewToken creates a new token
func NewToken(usr string) (Token, error) {
	claims := &TokenClaims{
		Usr: usr,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(
				time.Duration(cfg.Config.GetInt("tokens.lifespan")) * time.Minute,
			).Unix(),
		},
	}
	tkn := jwt.NewWithClaims(jwt.SigningMethodHS512, claims)
	tknStr, err := tkn.SignedString([]byte(cfg.Config.GetString("tokens.secret")))
	if err != nil {
		return "", fmt.Errorf("error singing the token: %v", err)
	}

	return Token(tknStr), nil
}

// Validate checks if the token is valid or not
func (t *Token) Validate() bool {
	claims := &TokenClaims{}

	tkn, err := jwt.ParseWithClaims(t.String(), claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(cfg.Config.GetString("tokens.secret")), nil
	})
	if err != nil || !tkn.Valid {
		return false
	}

	return true
}

// Renew renews the validity of the token
// TODO: Renew already expired tokens
func (t *Token) Renew() error {
	claims := &TokenClaims{}

	tkn, err := jwt.ParseWithClaims(t.String(), claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(cfg.Config.GetString("tokens.secret")), nil
	})
	if err != nil || !tkn.Valid {
		return errors.New("error renewing the token: the token is invalid or has already expired")
	}

	claims.ExpiresAt = time.Now().Add(
		time.Duration(cfg.Config.GetInt("tokens.lifespan")) * time.Minute,
	).Unix()

	tkn = jwt.NewWithClaims(jwt.SigningMethodHS512, claims)
	tknStr, err := tkn.SignedString([]byte(cfg.Config.GetString("tokens.secret")))
	if err != nil {
		return fmt.Errorf("error singing the token: %v", err)
	}

	*t = Token(tknStr)
	return nil
}

// String returns the token as a string
func (t Token) String() string {
	return string(t)
}
