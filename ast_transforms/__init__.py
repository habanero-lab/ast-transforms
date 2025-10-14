def add_func_decorator(tree, *args):
    '''Apply the `add_func_decorator` AST transform.'''
    from .passes import add_func_decorator as m
    return m.transform(tree, *args)

def attach_def_use_vars(tree, *args):
    '''Apply the `attach_def_use_vars` AST transform.'''
    from .passes import attach_def_use_vars as m
    return m.transform(tree, *args)

def remove_func_arg_annotation(tree, *args):
    '''Apply the `remove_func_arg_annotation` AST transform.'''
    from .passes import remove_func_arg_annotation as m
    return m.transform(tree, *args)

def remove_func_decorator(tree, *args):
    '''Apply the `remove_func_decorator` AST transform.'''
    from .passes import remove_func_decorator as m
    return m.transform(tree, *args)

def replace_name(tree, *args):
    '''Apply the `replace_name` AST transform.'''
    from .passes import replace_name as m
    return m.transform(tree, *args)

def to_single_op_form(tree, *args):
    '''Apply the `to_single_op_form` AST transform.'''
    from .passes import to_single_op_form as m
    return m.transform(tree, *args)

def where_to_ternary(tree, *args):
    '''Apply the `where_to_ternary` AST transform.'''
    from .passes import where_to_ternary as m
    return m.transform(tree, *args)

