import math
from . import NeuronMorphology


def test_neuronmorphology_empty_when_created():
    n = NeuronMorphology()
    assert len(n) == 0


def test_neuronmorphology_length():
    n = NeuronMorphology()
    n.add_node(1, 4, [1, 1, 1], 1)
    assert len(n) == 1


def test_neuronmorphology_from_string():
    n = NeuronMorphology.from_string(
        """
    0 1 2 3 4 -1
    """
    )
    assert len(n) == 1

    n = NeuronMorphology.from_string(
        """
    0 1 2 3 4 -1
    1 1 2 3 4 0
    """
    )
    assert len(n) == 2


def test_neuronmorphology_branch_count():

    n = NeuronMorphology.from_string(
        """
    0 1 2 3 4 -1
    1 1 2 3 4 0
    """
    )
    assert n.get_branch_points() == []
    n = NeuronMorphology.from_string(
        """
    0 1 2 3 4 -1
    1 1 2 3 4 0
    2 1 2 3 4 0
    """
    )
    assert n.get_branch_points() == [0]

    n = NeuronMorphology.from_string(
        """
    0 1 2 3 4 -1
    1 1 2 3 4 0
    2 1 2 3 4 0
    3 1 2 3 4 0
    """
    )
    assert n.get_branch_points() == [0]

    n = NeuronMorphology.from_string(
        """
    0 1 2 3 4 -1
    1 1 2 3 4 0
    2 1 2 3 4 0
    3 1 2 3 4 1
    4 1 2 3 4 1
    """
    )
    assert n.get_branch_points() == [0, 1]


def test_new_makes_copy():
    n = NeuronMorphology()
    n.add_node(1)
    m = NeuronMorphology(source=n)
    m.add_node(2)
    assert len(n) == 1
    assert len(m) == 2


def test_translate():
    n = NeuronMorphology()
    n.add_node(1, xyz=[0, 0, 5])
    n.translate([5, 10, 15], inplace=True)
    assert n.get_graph().nodes[1]["xyz"] == [5, 10, 20]


def test_rotate():
    n = NeuronMorphology()
    n.add_node(1, xyz=[0, 1, 5])
    n.rotate([0, 0, math.pi / 2], inplace=True)
    assert n.get_graph().nodes[1]["xyz"] == [-1, 0, 5]


def test_rotate():
    n = NeuronMorphology()
    n.add_node(1, xyz=[0, 1, 5])
    m = n.scale([100, 2, 3], inplace=False)
    assert n.get_graph().nodes[1]["xyz"] == [0, 1, 5]
    assert m.get_graph().nodes[1]["xyz"] == [0, 2, 15]
    assert n.scale(2).get_graph().nodes[1]["xyz"] == [0, 2, 10]
