package hyper

import (
	"fmt"
)

func (h *Hyper) DesktopResume(id string) error {
	if err := h.conn.DomainRestore(id); err != nil {
		return fmt.Errorf("resume desktop: %w", err)
	}

	return nil
}
