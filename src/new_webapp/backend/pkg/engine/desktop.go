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

package engine

import (
	"context"
	"fmt"

	"github.com/isard-vdi/isard/src/new_webapp/backend/pkg/models"
	"github.com/isard-vdi/isard/src/new_webapp/backend/proto/third_party/engine/desktop"
)

// DesktopStart starts a desktop
func (c *Client) DesktopStart(d *models.Desktop) error {
	req := &desktop.StartRequest{
		DesktopId: d.ID,
	}

	rsp, err := c.Desktop.Start(context.Background(), req)
	if err != nil {
		return fmt.Errorf("error starting %s: %v", d.ID, err)
	}

	d.State = rsp.State.String()
	d.Detail = rsp.Detail
	d.NextActions = rsp.NextActions

	return nil
}
