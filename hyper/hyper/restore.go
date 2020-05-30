package hyper

import (
	"fmt"
)

func (h *Hyper) DesktopRestore(savepath string) error {
	if err := h.conn.DomainRestore(savepath); err != nil {
		return fmt.Errorf("restore desktop: %w", err)
	}

	return nil
}
