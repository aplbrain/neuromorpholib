## *Class* `NodeTypes`


Enum of types for nodes in SWC.

range(8)


## *Function* `is_valid(cls, t: int) -> bool`


Determine if a node type is a valid SWC-spec type.

### Arguments
> - **t** (`int`: `None`): Type

### Returns
> - **bool** (`None`: `None`): True if valid



## *Class* `NeuronMorphology`


A wrapper class for neuron morphologies.

Contains a graph representation of the morphology in nx.DiGraph format.


## *Function* `__init__(self, **kwargs)`


Create a new NeuronMorphology.

### Arguments
> - **source** (`NeuronMorphology`: `None`): Optional. Source to copy from



## *Function* `get_graph(self, copy: bool = True) -> nx.DiGraph`


Return the underlying graph data structure.

By default, this returns a copy, so that modifications to this graph do not affect the parent NeuronMorphology (which is expected behavior). However, by explicitly passing `copy=False`, you can request a pointer to the same graph.

### Arguments
> - **True)** (`None`: `None`): If a copy should be returned instead of a
        pointer to the original

### Returns
> - **networkx.Graph** (`None`: `None`): The graph data structure that backs the morphology



## *Function* `add_edge(self, start: int, end: int) -> None`


Add a new edge to the skeleton.

### Arguments
> - **start** (`int`: `None`): The origin of the edge (ID)
> - **stop** (`int`: `None`): The end of the edge (ID)

### Returns
    None



## *Function* `get_branch_points(self) -> List[int]`


Returns a list of all node IDs where degree > 2.

### Arguments
    None

### Returns
> - **int[]** (`None`: `None`): Node IDs where degree > 2


## *Function* `get_branch_angle(self, abc)`


Returns the minimum branch angle between edges AB and BC.


## *Function* `smoothed(self) -> nx.DiGraph`


Returns a _copy_ of this morphology as a smoothed graph.
> - **TODO** (`None`: `None`): This is very inefficient.



## *Function* `translate(self, translation: Tuple[int, int, int], inplace=False)`


Translate the target neuron morphology (affine translation) in XYZ.

### Arguments
> - **int])** (`None`: `None`): The translation to perform
> - **inplace** (`bool`: `False`): Whether to perform the translation on this
        morphology (True) or on a copy (False).

### Returns
    The morphology upon which the translation was performed



## *Function* `scale(self, scale: Union[float, Tuple[float, float, float]], inplace=False)`


Scale the target neuron morphology.

### Arguments
> - **float]])** (`None`: `None`): The scale to
        perform. If a tuple, [X,Y,Z]. If a scalar, perform an isometric         scale on all three axes.
> - **inplace** (`bool`: `False`): Whether to perform the translation on this
        morphology (True) or on a copy (False).

### Returns
    The morphology upon which the scaling was performed



## *Function* `translate(self, translation: Tuple[int, int, int], inplace=False)`


Translate the target neuron morphology (affine translation) in XYZ.

### Arguments
> - **int])** (`None`: `None`): The translation to perform
> - **inplace** (`bool`: `False`): Whether to perform the translation on this
        morphology (True) or on a copy (False).

### Returns
    The morphology upon which the translation was performed



## *Function* `read_swc(swc_str: str) -> NeuronMorphology`


Construct a NeuronMorphology from a SWC string.

For file imports, see also `load_swc`.

### Returns
    NeuronMorphology


## *Function* `load_swc(filename: str) -> NeuronMorphology`


Loads a SWC from disk, into a NeuronMorphology object.

For str imports, see also `read_swc`.

### Arguments
    filename (str)

### Returns
    NeuronMorphology



## *Function* `save_swc(filename: str, nmorpho: str) -> str`


Saves a morphology to disk in the form of a SWC file.

### Arguments
> - **filename** (`str`: `None`): The file to which to save the SWC
> - **nmorpho** (`NeuronMorphology`: `None`): The morphology to save

### Returns
> - **str** (`None`: `None`): File path on disk to which the SWC was saved

