package hyper

func (h *Hyper) Restore(path string) error {
	return h.conn.DomainRestore(path)
}
