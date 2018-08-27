#!/usr/bin/enb python3
import requests
import glob

from .. import swc


class NeuroMorpho:

    def __init__(self, cache_location="~/.neuromorphocache/"):
        self.cache = {}
        self.cache_location = cache_location
        self.base_url = "http://neuromorpho.org/"
        self._permitted_fields = self.get_json("api/neuron/fields")['Neuron Fields']

    def url(self, ext=""):
        ext = ext.lstrip("/")
        return self.base_url + ext

    def get_json(self, ext):
        res = requests.get(self.url(ext))
        return res.json()

    def search(self, query, page=0, limit=None):
        for k, _ in query.items():
            if k not in self._permitted_fields:
                raise ValueError(
                    "Key {} is not a valid search parameter!\n".format(k) +
                    "Must be one of:\n{}".format(self._permitted_fields)
                )
        query_string = "&".join([
            "fq={}:{}".format(k, v) for k, v in query.items()
        ])

        listing = self.get_json("api/neuron/select/?" + query_string[1:] + "&page={}".format(page))
        try:
            results = listing["_embedded"]["neuronResources"]
            print("Downloading page {} for {} neurons, ending in {}".format(page, len(results), results[-1]['neuron_name']))
            neuron_listing = results
        except KeyError:
            return []

        if (
            "page" in listing and
            "totalPages" in listing["page"] and
            listing['page']['totalPages'] >= page
        ):
            if limit is None or len(neuron_listing) < limit:
                if limit is None:
                    neuron_listing += self.search(query, page=page+1)
                else:
                    neuron_listing += self.search(query, page=page+1, limit=limit-50)
            else:
                return neuron_listing

        return neuron_listing

    def download_swc(self, archive, neuron_name=None, text_only=False):

        if neuron_name is None and isinstance(archive, dict):
            return download_swc(archive['archive'], archive['neuron_name'], text_only)

        ext = "dableFiles/{}/CNG%20version/{}.CNG.swc".format(
            archive.lower(),
            neuron_name
        )
        res = requests.get(self.url(ext))
        if ("<html>" in res):
            raise ValueError("Failed to fetch from {}.".format(ext))

        if text_only:
            return res.text

        return swc.read_swc(res.text)
