# -*- coding: utf-8 -*-
PREFIX = "/api"

CORS_POLICY = {"origins": ("*",), "max_age": 3600}


class Base(object):
    def __init__(self, request):
        self.request = request

    @property
    def _index(self):
        return self.request.registry.settings["pyfapi.es.index"]

    def _result(self, result):
        return {"result": result, "error": ""}

    def _error(self, error):
        return {"result": {}, "error": error}

    def _read_cfg(self, name):
        return read_cfg(self.request.registry.settings["pyfapi.cfg_path"], name)
