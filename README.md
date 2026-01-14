# AST Transforms

A collection of Python AST-based code analysis and transformations.

## Installation

```bash
pip install astpass
```

## Usage

```python
import ast
import numpy as np
from astpass.passes import shape_analysis

tree = ast.parse("a + 1")
runtime_vals = {"a": np.random.randn(100)}
shape_info = shape_analysis.analyze(tree, runtime_vals)
for node, shape in shape_info.items():
    print(ast.unparse(node), shape)

##### Should print #####
# a (100,)
# 1 ()
# a + 1 (100,)
```

## Passes

* `shape_analysis` – returns a dictionary where each node is mapped to a shape.
* More passes are to be added ...
