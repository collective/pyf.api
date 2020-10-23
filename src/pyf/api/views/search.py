# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from cornice.resource import resource
from pyf.api.search import Search
from pyf.api.views.base import Base
from pyf.api.views.base import CORS_POLICY
from pyf.api.views.base import PREFIX

# import json
import logging


logger = logging.getLogger("pyf.api")


@resource(path=PREFIX + "/search", cors_policy=CORS_POLICY)
class SearchView(Base):
    def post(self):
        search_params = self.request.json_body
        if "classifiers" not in search_params:
            search_params["classifiers"] = []
        if "text" not in search_params:
            search_params["text"] = ""
        start = int(search_params.get("start", 0))
        size = int(search_params.get("size", 100))
        if size > 500:
            return self._error("Maximum batch size is 500!")
        try:
            search = Search(self.request.registry.settings, search_params, start, size)
            result = search.result()
        except Exception as e:
            logger.exception("Problem fetching result. {0}".format(e.with_traceback(None)))
            return self._error("Problem fetching result. {0}".format(e.with_traceback(None)))
        return self._result(result)
