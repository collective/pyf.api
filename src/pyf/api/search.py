# -*- coding: utf-8 -*-
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

    def result(self):
        search = self.search
        if self.params["classifiers"]:
            search = self.search.filter(
                "terms", **{"classifiers": self.params["classifiers"]}
            )
        if self.params["text"]:
            search = search.multimatch(
                query=self.params["text"],
                fields=["name^1.2", "summary^1.1", "description"],
            )
            search = search.sort('_score')
        else:
            search = search.sort('_score')

        # paginate
        search = search[self.start : self.start + self.size]

        response = search.execute()
        result = {
            "total": response["hits"]["total"],
            "start": self.start,
            "size": 0,
            "took": response["took"],
            "batch": [],
        }
        for hit in response["hits"]["hits"]:
            result["batch"].append(hit)
            result["size"] += 1
        import pdb; pdb.set_trace()
        return result
