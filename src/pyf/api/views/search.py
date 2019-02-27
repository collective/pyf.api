# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from pyf.api.search import Search
from pyf.api.views.base import Base
from pyf.api.views.base import CORS_POLICY
from pyf.api.views.base import PREFIX
from cornice.resource import resource

import json
import logging


logger = logging.getLogger(__name__)


@resource(path=PREFIX + "/search", cors_policy=CORS_POLICY)
class SearchView(Base):
    def post(self):
        search_params = json.loads(self.request.body)
        search = Search(
            self.request.registry.settings, search_params
        )
        return search.ui_result()
