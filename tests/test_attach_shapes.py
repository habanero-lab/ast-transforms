import ast
import textwrap
from ast_transforms.passes import shape_analysis
import numpy as np

def test_unary1():
    code = """
    -1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('1', ()), ('-1', ())]

def test_unary2():
    code = """
    -1.0
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('1.0', ()), ('-1.0', ())]

def test_unary3():
    code = """
    -a
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": 1}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('-a', ())]

def test_unary4():
    code = """
    -a
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(10)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (10,)), ('-a', (10,))]

def test_binary1():
    code = """
    1 + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('1', ()), ('1', ()), ('1 + 1', ())]

def test_binary2():
    code = """
    1.0 + 1.0
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('1.0', ()), ('1.0', ()), ('1.0 + 1.0', ())]

def test_binary3():
    code = """
    a + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": 1}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('1', ()), ('a + 1', ())]

def test_binary4():
    code = """
    a + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.int32(1)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('1', ()), ('a + 1', ())]

def test_binary5():
    code = """
    a + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('1', ()), ('a + 1', (100,))]

def test_binary6():
    code = """
    a + b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('a + b', (100,))]

def test_binary7():
    code = """
    a + b * 2 - 1
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('2', ()), ('b * 2', (100,)), \
        ('a + b * 2', (100,)), ('1', ()), ('a + b * 2 - 1', (100,))]
    
def test_binary8():
    code = """
    a / 2 - b // 2
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('2', ()), ('a / 2', (100,)), \
        ('b', (100,)), ('2', ()), ('b // 2', (100,)), ('a / 2 - b // 2', (100,))]

def test_binary9():
    code = """
    a @ b
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {"a": np.random.randn(100), "b": np.random.randn(100)}
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('a @ b', ())]

def test_call_np_add1():
    code = """
    np.add(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100), 
        "b": np.random.randn(100),
        "np": np
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('np.add(a, b)', (100,))]

def test_call_pow1():
    code = """
    pow(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": 2, 
        "b": 3,
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('b', ()), ('pow(a, b)', ())]

def test_call_pow2():
    code = """
    pow(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
        "b": 3,
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', ()), ('pow(a, b)', (100,))]

def test_call_pow3():
    code = """
    pow(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
        "b": np.ones(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('pow(a, b)', (100,))]

def test_call_np_pow1():
    code = """
    np.pow(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": 2, 
        "b": 3,
        "np": np
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', ()), ('b', ()), ('np.pow(a, b)', ())]

def test_call_np_pow2():
    code = """
    np.pow(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
        "b": 3,
        "np": np
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', ()), ('np.pow(a, b)', (100,))]

def test_call_np_pow3():
    code = """
    np.pow(a, b)
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
        "b": np.ones(100),
        "np": np
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items()]
    assert results == [('a', (100,)), ('b', (100,)), ('np.pow(a, b)', (100,))]

def test_slice1():
    code = """
    a[0:2]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [('0:2', (2,))]

def test_slice2():
    code = """
    a[:2]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [(':2', (2,))]

def test_slice3():
    code = """
    a[:]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [(':', (None,))]

def test_slice4():
    code = """
    a[0:]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [('0:', (None,))]

def test_slice5():
    code = """
    a[1:]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [('1:', (-1,))]

def test_slice6():
    code = """
    a[1:-1]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [('1:-1', (-2,))]

def test_slice7():
    code = """
    a[:-1]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Slice)]
    assert results == [(':-1', (-1,))]

def test_subscript1():
    code = """
    a[0:2]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[0:2]', (2,))]

def test_subscript2():
    code = """
    a[:2]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[:2]', (2,))]

def test_subscript3():
    code = """
    a[:]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[:]', (100,))]

def test_subscript4():
    code = """
    a[0:]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[0:]', (100,))]

def test_subscript5():
    code = """
    a[1:]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[1:]', (99,))]

def test_subscript6():
    code = """
    a[1:-1]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[1:-1]', (98,))]

def test_subscript7():
    code = """
    a[:-1]
    """
    tree = ast.parse(textwrap.dedent(code))
    rt_vals = {
        "a": np.random.randn(100),
    }
    shape_info = shape_analysis.visit(tree, rt_vals)
    results = [(ast.unparse(node), shape) for node, shape in shape_info.items() if isinstance(node, ast.Subscript)]
    assert results == [('a[:-1]', (99,))]

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