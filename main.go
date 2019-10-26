package main

import (
	_ "github.com/Ksos-org/ksos-api/routers"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
	_ "github.com/astaxie/beego/orm"
	_ "github.com/lib/pq"
)

func init() {
	_ = orm.RegisterDriver("postgres", orm.DRPostgres)

	_ = orm.RegisterDataBase("default", "postgres", "dbname=postgres host=localhost user=postgres password=postgres port=5432 sslmode=disable")
}

func main() {
	if beego.BConfig.RunMode == "dev" {
		beego.BConfig.WebConfig.DirectoryIndex = true
		beego.BConfig.WebConfig.StaticDir["/swagger"] = "swagger"
	}
	beego.Run()
}
