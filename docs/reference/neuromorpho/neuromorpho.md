## *Class* `NeuroMorpho`


A class that manages remote queries and downloads from a NeuronMorphology server, such as neuromorpho.org.

.


## *Function* `__init__(self, cache_location: str = "~/.neuromorphocache/") -> None`


Construct a new NeuroMorpho.

### Arguments
> - **cache_location** (`str`: `None`): Where to store SWC files after download



## *Function* `url(self, ext: str = "") -> str`


Construct a URL with the base_url of this remote as prefix.

.


## *Function* `get_json(self, ext: str) -> dict`


Get JSON from a GET request.

.


## *Function* `search(self, query: dict, page: int = 0, limit: int = None) -> List`


Search the remote for a query (dict).

.


## *Function* `get_neuron_info(self, neuron_name: Union[str, int]) -> dict`


http://www.neuromorpho.org/api/neuron/name/{name}
