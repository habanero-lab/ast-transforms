import ast
import textwrap
import numpy as np

from ast_transforms.passes import array_expr_to_loop

def test_add1():
    code = """
    c = a + b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        'a': np.random.randn(10),
        'b': 2,
        'c': np.empty(10)
    }
    tree = array_expr_to_loop.transform(tree, rt_vals)

    expected = """
    for i in range(10):
        c[i] = a[i] + b
    """
    new_code = ast.unparse(tree)
    assert new_code == ast.unparse(ast.parse(textwrap.dedent(expected)))