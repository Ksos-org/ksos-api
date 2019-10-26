package routers

import (
	"github.com/Ksos-org/ksos-api/controllers"
	"github.com/astaxie/beego"
)

func init() {
    beego.Router("/", &controllers.MainController{})
}
