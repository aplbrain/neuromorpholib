#!/usr/bin/env python3
"""
SWC: Manipulate graph data in SWC format.

Includes read/write to disk.
"""
from typing import List, Tuple, Union
import math

import networkx as nx


class NodeTypes:
    """
    Enum of types for nodes in SWC.

    range(8)
    """

    UNDEFINED = 0
    SOMA = 1
    AXON = 2
    DENDRITE = 3
    APICAL_DENDRITE = 4
    FORK_POINT = 5
    END_POINT = 6
    CUSTOM = 7

    @staticmethod
    def is_valid(cls, t: int) -> bool:
        """
        Determine if a node type is a valid SWC-spec type.

        Arguments:
            t (int): Type

        Returns:
            bool: True if valid

        """
        return t in [0, 1, 2, 3, 4, 5, 6, 7]


class NeuronMorphology:
    """
    A wrapper class for neuron morphologies.

    Contains a graph representation of the morphology in nx.DiGraph format.
    """

    def __init__(self, **kwargs):
        """
        Create a new NeuronMorphology.

        Arguments:
            source (NeuronMorphology): Optional. Source to copy from

        """
        if "source" in kwargs:
            if isinstance(kwargs["source"], NeuronMorphology):
                self._skeleton = kwargs["source"].get_graph()
            elif isinstance(kwargs["source"], nx.Graph):
                self._skeleton = kwargs["source"]
            else:
                raise ValueError(
                    "The `source` argument passed to the NeuronMorphology "
                    + "constructor must be a graph or a NeuronMorphology."
                    + "Type was {}.".format(type(kwargs["source"]))
                )
        else:
            self._skeleton = nx.DiGraph()

    def __len__(self):
        return len(self._skeleton)

    def get_graph(self, copy: bool = True) -> nx.DiGraph:
        """
        Return the underlying graph data structure.

        By default, this returns a copy, so that modifications to this graph do
        not affect the parent NeuronMorphology (which is expected behavior).
        However, by explicitly passing `copy=False`, you can request a pointer
        to the same graph.

        Arguments:
            copy (bool : True): If a copy should be returned instead of a
                pointer to the original

        Returns:
            networkx.Graph: The graph data structure that backs the morphology

        """
        if copy:
            return self._skeleton.copy()
        else:
            return self._skeleton

    def add_node(
        self, id: int, t: int = None, xyz: Tuple[int, int, int] = None, r: float = None
    ) -> None:
        """
        Add a new node to the skeleton.

        Arguments:
            id (int): The ID of the node (0 is invalid)
            t (int): The type of node. Validate with `NodeTypes.is_valid(t)`
            xyz (int[3]): The xyz position of the node
            r (float): The radius of the neuron at this node

        Returns:
            None
        """
        return self._skeleton.add_node(id, t=t, xyz=xyz, r=r)

    def add_edge(self, start: int, end: int) -> None:
        """
        Add a new edge to the skeleton.

        Arguments:
            start (int): The origin of the edge (ID)
            stop (int): The end of the edge (ID)

        Returns:
            None

        """
        return self._skeleton.add_edge(start, end)

    def get_branch_points(self) -> List[int]:
        """
        Returns a list of all node IDs where degree > 2.

        Arguments:
            None

        Returns:
            int[]: Node IDs where degree > 2
        """
        results: List[int] = []
        for start, stops in self._skeleton.pred.items():
            if len(stops.keys()) >= 2:
                results.append(start)
        return results

    def get_branch_angle(self, abc):
        """
        Returns the minimum branch angle between edges AB and BC.
        """
        raise NotImplementedError

    def smoothed(self) -> nx.DiGraph:
        """
        Returns a _copy_ of this morphology as a smoothed graph.
        # TODO: This is very inefficient.

        """
        gcopy = self.get_graph()
        gcopy_old = self.get_graph()
        new_count = 0
        old_count = len(self._skeleton.adj)
        while new_count != old_count:
            gcopy_old = gcopy
            old_count = len(gcopy_old.adj)
            for node, connections in gcopy_old.adj.items():
                if len(connections) == 2:
                    start, stop = connections.keys()
                    gcopy.add_edge(start, stop)
                    gcopy.remove_node(node)
                    break
            new_count = len(gcopy.adj)
        return gcopy

    @staticmethod
    def from_file(filename: str):
        return load_swc(filename)

    @staticmethod
    def from_string(swc: str):
        return read_swc(swc)

    def translate(self, translation: Tuple[int, int, int], inplace=False):
        """
        Translate the target neuron morphology (affine translation) in XYZ.

        Arguments:
            translation (Tuple[int, int, int]): The translation to perform
            inplace (bool: False): Whether to perform the translation on this
                morphology (True) or on a copy (False).

        Returns:
            The morphology upon which the translation was performed

        """
        if inplace:
            target = self
        else:
            target = NeuronMorphology(source=self)
        for node in target._skeleton.nodes():
            current = target._skeleton.nodes[node]["xyz"]
            target._skeleton.nodes[node]["xyz"] = [
                current[0] + translation[0],
                current[1] + translation[1],
                current[2] + translation[2],
            ]
        return target

    def scale(self, scale: Union[float, Tuple[float, float, float]], inplace=False):
        """
        Scale the target neuron morphology.

        Arguments:
            scale (Union[float, Tuple[float, float, float]]): The scale to
                perform. If a tuple, [X,Y,Z]. If a scalar, perform an isometric
                scale on all three axes.
            inplace (bool: False): Whether to perform the translation on this
                morphology (True) or on a copy (False).

        Returns:
            The morphology upon which the scaling was performed

        """
        if inplace:
            target = self
        else:
            target = NeuronMorphology(source=self)

        if isinstance(scale, (float, int)):
            scale = [scale, scale, scale]

        for node in target._skeleton.nodes():
            current = target._skeleton.nodes[node]["xyz"]
            target._skeleton.nodes[node]["xyz"] = [
                current[0] * scale[0],
                current[1] * scale[1],
                current[2] * scale[2],
            ]
        return target

    def translate(self, translation: Tuple[int, int, int], inplace=False):
        """
        Translate the target neuron morphology (affine translation) in XYZ.

        Arguments:
            translation (Tuple[int, int, int]): The translation to perform
            inplace (bool: False): Whether to perform the translation on this
                morphology (True) or on a copy (False).

        Returns:
            The morphology upon which the translation was performed

        """
        if inplace:
            target = self
        else:
            target = NeuronMorphology(source=self)
        for node in target._skeleton.nodes():
            current = target._skeleton.nodes[node]["xyz"]
            target._skeleton.nodes[node]["xyz"] = [
                current[0] + translation[0],
                current[1] + translation[1],
                current[2] + translation[2],
            ]
        return target

    def rotate(
        self, rotation: Tuple[int, int, int], inplace: bool = False, _p: int = 10
    ):
        """
        Perform a rotation on the neuron morphology.

        If inplace is True, will perform the rotation on the current object.

        Arguments:
            rotation (Tuple[int, int, int]): The rotation to perform, in
                pitch-roll-yaw order. Units are in radians.
            inplace (bool: False): Whether to perform the rotation on this
                morphology (True) or on a copy (False).
            _p (int: 10): Digits of precision. Because SWC files are text-
                files, higher precision here costs more in terms of file
                storage. Values of 5 or greater should be fine for most
                purposes, unless coordinates are small to begin with.

        Returns:
            The morphology upon which the translation was performed

        """

        # Formula adapted from https://stackoverflow.com/a/34060479/979255
        pitch, roll, yaw = rotation
        cosa = math.cos(yaw)
        sina = math.sin(yaw)

        cosb = math.cos(pitch)
        sinb = math.sin(pitch)

        cosc = math.cos(roll)
        sinc = math.sin(roll)

        Axx = cosa * cosb
        Axy = cosa * sinb * sinc - sina * cosc
        Axz = cosa * sinb * cosc + sina * sinc

        Ayx = sina * cosb
        Ayy = sina * sinb * sinc + cosa * cosc
        Ayz = sina * sinb * cosc - cosa * sinc

        Azx = -sinb
        Azy = cosb * sinc
        Azz = cosb * cosc

        if inplace:
            target = self
        else:
            target = NeuronMorphology(source=self)

        for node in target._skeleton.nodes():
            current = target._skeleton.nodes[node]["xyz"]
            target._skeleton.nodes[node]["xyz"] = [
                math.round(Axx * current[0] + Axy * current[1] + Axz * current[2], _p),
                math.round(Ayx * current[0] + Ayy * current[1] + Ayz * current[2], _p),
                math.round(Azx * current[0] + Azy * current[1] + Azz * current[2], _p),
            ]


def read_swc(swc_str: str) -> NeuronMorphology:
    """
    Construct a NeuronMorphology from a SWC string.

    For file imports, see also `load_swc`.

    Returns:
        NeuronMorphology
    """
    lines = swc_str.split("\n")
    neuron = NeuronMorphology()
    last_index = None
    for line in lines:
        line = line.strip()
        if (not line) or (line[0] == "#"):
            continue
        else:
            attrs = [float(i) for i in line.split()]
            neuron.add_node(int(attrs[0]), t=int(attrs[1]), xyz=attrs[2:5], r=attrs[5])
            last_index = attrs[-1]
            if last_index >= 0:
                neuron.add_edge(int(attrs[0]), int(attrs[-1]))
    return neuron


def load_swc(filename: str) -> NeuronMorphology:
    """
    Loads a SWC from disk, into a NeuronMorphology object.

    For str imports, see also `read_swc`.

    Arguments:
        filename (str)

    Returns:
        NeuronMorphology

    """
    try:
        with open(filename, "r") as fh:
            contents = fh.read()
            return read_swc(contents)
    except Exception as ex:
        raise ValueError("Invalid file {}".format(filename))


def save_swc(filename: str, nmorpho: str) -> str:
    """
    Saves a morphology to disk in the form of a SWC file.

    Arguments:
        filename (str): The file to which to save the SWC
        nmorpho (NeuronMorphology): The morphology to save

    Returns:
        str: File path on disk to which the SWC was saved

    """
    lines = []
    _edges = nmorpho.get_graph().edges()
    # Loop through the nodes. Pass `True` to include metadata:
    for node in nmorpho.get_graph().nodes_iter(True):
        parent = nmorpho.get_graph().edges([node[0]])
        if parent == []:
            parent = -1
        else:
            parent = parent[0][1]

        #             n  T xyz R  P
        lines.append(
            "{} {} {} {} {}".format(
                str(node[0]),
                str(node[1]["t"]),
                " ".join([str(i) for i in node[1]["xyz"]]),
                str(node[1]["r"]),
                str(parent),
            )
        )
    with open(filename, "w") as swc_output:
        swc_output.write("\n".join(lines))
        swc_output.write("\n")
    return filename
