# -*- coding: utf-8 -*-
from collections import OrderedDict
from itertools import islice
from pyf.api.utils import get_search


def sort_on_score(search, order):
    return search.sort({"_score": order})


class Search(object):
    def __init__(self, settings, params, start, size):
        self.settings = settings
        self.params = params
        self.index = settings["pyfapi.es.index"]
        self.search = get_search(settings)
        self.start = start
        self.size = size

    def _build_search(self):
        search = self.search
        if self.params["classifiers"]:
            search = self.search.filter(
                "terms", **{"classifiers": self.params["classifiers"]}
            )
        if self.params["text"]:
            search = search.query(
                "query_string",
                query=self.params["text"],
                fields=["name^2", "summary^1.2", "description"],
            )
        search = search.sort(
            "_score",
            "name_sorted",
            {"version_major": "desc"},
            {"version_minor": "desc"},
            {"version_bugfix": "desc"},
            {"version_postfix": "desc"},
            {"version_raw": "desc"},
        )
        # we want the newest of an addon
        # this can be done by field collapsing
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-collapse
        search = search.extra(
            collapse={
                "field": "name",
            },
        )
        return search

    def result(self):
        search = self._build_search()
        collector = OrderedDict()
        for hit in search.execute():
            key = "{0}|{1}".format(hit["name"], hit["version"])
            # print(hit['version_major'],hit['version_minor'],hit['version_bugfix'],hit['version_postfix'],)
            collector[key] = hit
        result = {
            "total": len(collector),
            "start": self.start,
            "size": 0,
            "batch": [],
        }
        for name, hit in islice(collector.items(), self.start, self.start + self.size):
            result["batch"].append(hit.to_dict())
            result["size"] += 1
        return result
