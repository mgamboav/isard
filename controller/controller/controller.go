package controller

import (
	"github.com/isard-vdi/isard/controller/client"
	"github.com/isard-vdi/isard/controller/env"

	"github.com/isard-vdi/isard/desktop-builder/desktopbuilder"
)

type Interface interface {
	// func DesktopList()
	DesktopStart(id string) (*desktopbuilder.Viewer, error)
}

type Controller struct {
	env *env.Env

	client *client.Client
}

func New(env *env.Env) *Controller {
	return &Controller{env: env}
}
