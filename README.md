# neuromorpholib


## Usage
A simple download of known dataset and name:
```python
from neuromorpholib import neuromorpho

nmo = neuromorpho.NeuroMorpho()
acc1 = nmo.download_swc("martone", "ACC1")
```

A query for all species=mouse neurons:
```python
mouse_neurons = nmo.search({"species": "mouse"})
```

Download a SWC for a mouse neuron:
```python
swc_demo = nmo.download_swc(
    mouse_neurons[0]['archive'],
    mouse_neurons[0]['neuron_name']
)
```
