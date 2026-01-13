import ast
import textwrap
from ast_transforms.passes import add_func_decorator

def test1():
    code = """
    def foo():
        return 42
    """
    tree = ast.parse(textwrap.dedent(code))
    new_tree = add_func_decorator.transform(tree, "jit")
    new_code = ast.unparse(new_tree)

    expected = """
    @jit
    def foo():
        return 42
    """
    assert new_code == ast.unparse(ast.parse(textwrap.dedent(expected)))

def test2():
    code = """
    def foo():
        return 42
    """
    tree = ast.parse(textwrap.dedent(code))
    new_tree = add_func_decorator.transform(tree, "numba.njit(parallel=True)")
    new_code = ast.unparse(new_tree)

    expected = """
    @numba.njit(parallel=True)
    def foo():
        return 42
    """
    assert new_code == ast.unparse(ast.parse(textwrap.dedent(expected)))
