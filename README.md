# neuromorpholib

[![Codecov](https://img.shields.io/codecov/c/github/aplbrain/neuromorpholib?style=for-the-badge)](https://codecov.io/gh/aplbrain/neuromorpholib)
[![PyPI](https://img.shields.io/pypi/v/neuromorpholib?style=for-the-badge)](https://pypi.org/project/neuromorpholib/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/aplbrain/neuromorpholib/Python%20Tests?style=for-the-badge)](https://github.com/aplbrain/neuromorpholib/actions?query=workflow%3A%22Python+Tests%22)

## Installation

```shell
pip3 install neuromorpholib
```

## Usage

### Downloading

#### A simple download of known dataset and name

```python
from neuromorpholib import neuromorpho

nmo = neuromorpho.NeuroMorpho()
acc1 = nmo.download_swc("martone", "ACC1")
```

#### A query for all species=mouse neurons

```python
mouse_neurons = nmo.search({"species": "mouse"})
```

#### Download a SWC for a mouse neuron

```python
swc_demo = nmo.download_swc(
    mouse_neurons[0]
)
```

If you know the archive name and neuron name, you can also download the swc directly by passing `archive` and `neuron_name` arguments.

If you only want the SWC text and don't want it to be converted into a `NeuronMorphology` object, you can pass `text_only=True`.

### SWC Management

#### Read a SWC file from disk

```python
from neuromorpholib.swc import load_swc, NeuronMorphology

my_morphology = load_swc("my_neuron.swc")
# This is a NeuronMorphology object.
```

#### Get a list of branch points

```python
branch_points = my_morphology.get_branch_points()
```

#### Get a simplified graph (only leaves and branch points) of a morphology

```python
morphology_graph = my_morphology.smoothed()
# nx.DiGraph
```

#### SWC Geometry Operations

Rotate, translate, or scale a geometry with `NeuronMorphology` functions:

```python
n = NeuronMorphology()
n.scale(3)
n.translate([4, 44, 10])
n.rotate([0, 0, math.pi/2])
```
