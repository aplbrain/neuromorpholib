"""
SWC: Manipulate graph data in SWC format.

Includes read/write to disk.
"""

import networkx as nx
import numpy as np


class NodeTypes:
    """
    Enum of types for nodes in SWC.

    range(7)
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
    def is_valid(cls, t):
        """
        Determine if a node type is a valid SWC-spec type.

        Arguments:
            t (int): Type

        Returns:
            bool: True if valid

        """
        return t in [0, 1, 2, 3, 4, 5, 6, 7]


class NeuronMorphology:

    def __init__(self, **kwargs):
        if 'source' in kwargs:
            if isinstance(kwargs['source'], NeuronMorphology):
                self._skeleton = kwargs['source'].get_graph()
            elif isinstance(kwargs['source'], nx.Graph):
                self._skeleton = kwargs['source']
            else:
                raise ValueError(
                    "The `source` argument passed to the NeuronMorphology " +
                    "constructor must be a graph or a NeuronMorphology." +
                    "Type was {}.".format(type(kwargs['source']))
                )
        else:
            self._skeleton = nx.DiGraph()

    def get_graph(self, copy=True):
        """
        Returns the underlying graph data structure. By default, it returns
        a copy, so that modifications to this graph do not affect the parent
        NeuronMorphology (which is expected behavior). However, by explicitly
        passing `copy=False`, you can request a pointer to the same graph.

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

    def add_node(self, id, t=None, xyz=None, r=None):
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

    def add_edge(self, start, end):
        """
        Add a new edge to the skeleton.

        Arguments:
            start (int): The origin of the edge (ID)
            stop (int): The end of the edge (ID)

        Returns:
            None

        """
        return self._skeleton.add_edge(start, end)

    def get_branch_points(self):
        """
        Returns a list of all node IDs where degree > 2.

        Arguments:
            None

        Returns:
            int[]: Node IDs where degree > 2
        """
        results = []
        for start, stops in self._skeleton.adj.items():
            if len(stops.keys()) > 2:
                results.append(start)
        return results

    def get_branch_angle(self, abc):
        """
        Returns the minimum branch angle between edges AB and BC.
        """
        raise NotImplementedError

    def smoothed(self):
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
                if len(connections) is 2:
                    start, stop = connections.keys()
                    gcopy.add_edge(start, stop)
                    gcopy.remove_node(node)
                    break
            new_count = len(gcopy.adj)
        return gcopy


def read_swc(swc_str):
    """
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
            neuron.add_node(
                int(attrs[0]),
                t=int(attrs[1]),
                xyz=attrs[2:5],
                r=attrs[5]
            )
            last_index = attrs[-1]
            if last_index > 0:
                neuron.add_edge(
                    int(attrs[0]),
                    int(attrs[-1])
                )
    return neuron


def load_swc(filename):
    """
    Loads a SWC from disk, into a NeuronMorphology object.

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


def save_swc(filename, nmorpho):
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
        lines.append("{} {} {} {} {}".format(
            str(node[0]),
            str(node[1]['t']),
            " ".join([str(i) for i in node[1]['xyz']]),
            str(node[1]['r']),
            str(parent)
        ))
    with open(filename, 'w') as swc_output:
        swc_output.write('\n'.join(lines))
        swc_output.write('\n')
    return filename
