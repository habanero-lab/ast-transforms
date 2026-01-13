import ast
import textwrap
from ast_transforms.passes import hoist_shape_access

def test1():
    code = """
    for i in range(a.shape[0]):
        x = a.shape[0] + b.shape[1]
        y = a[i] + b[i]
    """
    expected = """
    a_shape_0 = a.shape[0]
    b_shape_1 = b.shape[1]
    for i in range(a_shape_0):        
        x = a_shape_0 + b_shape_1
        y = a[i] + b[i]
    """
    tree = ast.parse(textwrap.dedent(code))
    tree = hoist_shape_access.transform(tree)
    assert ast.dump(tree) == ast.dump(ast.parse(textwrap.dedent(expected)))

def test2():
    code = """
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            b[i,j] = a[i,j] + 1
    """
    expected = """
    a_shape_0 = a.shape[0]
    a_shape_1 = a.shape[1]
    for i in range(a_shape_0):
        for j in range(a_shape_1):
            b[i,j] = a[i,j] + 1
    """
    tree = ast.parse(textwrap.dedent(code))
    tree = hoist_shape_access.transform(tree)
    print(ast.unparse(tree))
    assert ast.dump(tree) == ast.dump(ast.parse(textwrap.dedent(expected)))

