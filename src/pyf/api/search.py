# -*- coding: utf-8 -*-
from pyf.api.utils import get_search


def sort_on_score(search, order):
    return search.sort({'_score': order})


class Search(object):

    def __init__(self, settings, params):
        self.settings = settings
        self.params = params
        self.index = settings['presenter.es.index']
        self.search = get_search(settings)

