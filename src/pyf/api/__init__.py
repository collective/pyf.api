# -*- coding: utf-8 -*-
from pathlib import Path
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if not isinstance(settings["pyfapi.cfg_path"], Path):
        cfgpath = Path(settings["pyfapi.cfg_path"])
        settings["pyfapi.cfg_path"] = cfgpath
    config_params = {"settings": settings}
    config = Configurator(**config_params)
    config.include("cornice")
    config.scan()
    return config.make_wsgi_app()
