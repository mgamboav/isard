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

package tests_test

import (
	"net"
	"strconv"
	"testing"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/utils/tests"
)

func TestGetFreePort(t *testing.T) {
	port, err := tests.GetFreePort()
	if err != nil {
		t.Error(err)
	}
	if port == 0 {
		t.Error("port == 0")
	}

	// Try to listen on the port
	l, err := net.Listen("tcp", "localhost"+":"+strconv.Itoa(port))
	if err != nil {
		t.Error(err)
	}
	defer l.Close()
}
