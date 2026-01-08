import ast
import textwrap
from ast_transforms.passes import shape_analysis
import numpy as np

def test1():
    code = """
    1 + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('1', ()), ('1', ()), ('1 + 1', ())]

def test2():
    code = """
    1.0 + 1.0
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('1.0', ()), ('1.0', ()), ('1.0 + 1.0', ())]

def test3():
    code = """
    a + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": 1}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('1', ()), ('a + 1', ())]

def test4():
    code = """
    a + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.int32(1)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('1', ()), ('a + 1', ())]

def test5():
    code = """
    a + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('1', ()), ('a + 1', (100,))]

def test6():
    code = """
    a + b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('a + b', (100,))]

def test7():
    code = """
    a + b + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('a + b', (100,)), ('1', ()), ('a + b + 1', (100,))]

def test8():
    code = """
    a @ b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('a @ b', ())]


def test10():
    code = """
    c = a + b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        'a': 1,
        'b': 2
    }

    shape_info = shape_analysis.visit(tree)
    for node, shape in shape_info.items():
        assert shape == ()


def test12():
    code = """
    c = a + b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        'a': np.random.randn(100),
        'b': np.random.randn(100)
    }

    shape_info = shape_analysis.visit(tree)
    for node, shape in shape_info.items():
        assert shape == (100,)


def test13():
    code = """
    c = a[i] + b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        'a': np.random.randn(100),
        'b': 1.0,
        'i': 0
    }

    shape_info = shape_analysis.visit(tree)
    for node, shape in shape_info.items():
        if isinstance(node, ast.Name) and node.id == 'a':
            assert shape == (100,)
        else:
            assert shape == ()