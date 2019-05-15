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

package grpc

import (
	"testing"

	isard "github.com/isard-vdi/isard/src/new_webapp/backend/proto"

	"github.com/stretchr/testify/assert"
)

func TestParseState(t *testing.T) {
	assert := assert.New(t)

	t.Run("should return the correct state", func(t *testing.T) {
		state := parseState("STARTED")
		assert.Equal(isard.DesktopState_STARTED, state)
	})

	t.Run("should return the correct state if the state is STOPPED (0)", func(t *testing.T) {
		state := parseState("STOPPED")
		assert.Equal(isard.DesktopState_STOPPED, state)
	})

	t.Run("should return unknown if the state is not vaild", func(t *testing.T) {
		state := parseState("invalid state")
		assert.Equal(isard.DesktopState_UNKNOWN, state)
	})
}
