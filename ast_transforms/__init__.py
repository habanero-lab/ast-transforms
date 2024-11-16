import inspect, importlib

def apply_transform_on_ast(tree, m, *args):
    assert inspect.ismodule(m) or isinstance(m, str)
    if isinstance(m, str):
        module_name = f"ast_transforms.{m}"
        m = importlib.import_module(module_name)
    tree = m.transform(tree, *args)
    return tree