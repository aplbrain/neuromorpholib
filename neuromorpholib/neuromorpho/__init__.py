#!/usr/bin/env python3

from typing import List, Union
import requests
import glob

from .. import swc


class NeuroMorpho:
    """
    A class that manages remote queries and downloads from a NeuronMorphology
    server, such as neuromorpho.org.

    .
    """

    def __init__(self, cache_location: str = "~/.neuromorphocache/") -> None:
        """
        Construct a new NeuroMorpho.

        Arguments:
            cache_location (str): Where to store SWC files after download

        """
        self.cache = {}
        self.cache_location = cache_location
        self.base_url = "http://neuromorpho.org/"
        self._permitted_fields = self.get_json("api/neuron/fields")['Neuron Fields']

    def url(self, ext: str = "") -> str:
        """
        Construct a URL with the base_url of this remote as prefix.

        .
        """
        ext = ext.lstrip("/")
        return self.base_url + ext

    def get_json(self, ext: str) -> dict:
        """
        Get JSON from a GET request.

        .
        """
        res = requests.get(self.url(ext))
        return res.json()

    def search(self, query: dict, page: int = 0, limit: int = None) -> List:
        """
        Search the remote for a query (dict).

        .
        """
        for k, _ in query.items():
            if k not in self._permitted_fields:
                raise ValueError(
                    "Key {} is not a valid search parameter!\n".format(k) +
                    "Must be one of:\n{}".format(self._permitted_fields)
                )
        query_string = "&".join([
            "fq={}:{}".format(k, v) for k, v in query.items()
        ])

        listing = self.get_json(
            "api/neuron/select/?" + query_string[1:] + "&page={}".format(page)
        )
        try:
            results = listing["_embedded"]["neuronResources"]
            print(
                "Downloading page {} for {} neurons, ending in {}".format(
                    page, len(results), results[-1]['neuron_name']
                )
            )
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

    def download_swc(
            self, archive: str, neuron_name: str = None, text_only: bool = False
    ) -> Union[str, 'NeuronMorphology']:
        """
        Download a SWC file (or SWC string).

        Optionally convert into a NeuroMorpho object.
        """
        if neuron_name is None and isinstance(archive, dict):
            return self.download_swc(
                archive['archive'], archive['neuron_name'], text_only
            )
        if neuron_name is None and isinstance(archive, int):
            data = self.get_neuron_info(archive)
            return self.download_swc(
                data['archive'], data['neuron_name'], text_only
            )
        ext = "dableFiles/{}/CNG%20version/{}.CNG.swc".format(
            archive.lower(),
            neuron_name
        )
        res = requests.get(self.url(ext))
        if ("<html>" in res.text):
            raise ValueError("Failed to fetch from {}.".format(ext))

        if text_only:
            return res.text

        return swc.read_swc(res.text)

    def get_neuron_info(self, neuron_name: Union[str, int]) -> dict:
        """
        http://www.neuromorpho.org/api/neuron/name/{name}
        """
        if isinstance(neuron_name, int):
            return self.get_json("api/neuron/id/{}".format(neuron_name))
        else:
            return self.get_json("api/neuron/name/{}".format(neuron_name))
