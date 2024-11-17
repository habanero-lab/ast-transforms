import ast
import copy

def dump(tree):
    print(ast.dump(tree))

def dump_code(node):
    print(ast.unparse(node))

def new_ast_const(val):
    return ast.Constant(value=val)

def new_ast_for(target, range_node, body=None):
    realbody = body if body is not None else []
    loop = ast.For(target=target, iter=range_node, body=realbody, lineno=None,
        orelse=[], type_ignores=[])
    return loop

def new_ast_perfect_for(targets, range_nodes, body=None):
    parent = root = ast.Module(body=[])
    for tar, rg in zip(targets, range_nodes):
        loop = new_ast_for(tar, rg)
        parent.body.append(loop)
        parent = loop
    
    if body is not None:
        parent.body.extend(body)
    return root.body[0]

def new_ast_call(name_node, args, keywords=None):
    kws = []
    if keywords:
        for k, v in keywords.items():
            kws.append(ast.keyword(arg=k, value=v))
    if type(args) != list:
        args = [args]
    node = ast.Call(func=name_node, args=args, keywords=kws)
    return node

def new_ast_range(stop, start=new_ast_const(0), step=new_ast_const(1)):
    node = ast.Call(func=new_ast_name('range'), args=[start, stop, step], keywords=[])
    return node

def new_ast_node_from_str(s, inline=True):
    expr = ast.parse(s).body[0]
    if inline:
        return expr.value
    else:
        return expr

def new_ast_name(name, ctx=None):
    ctx = ast.Load() if ctx == None else ctx
    return ast.Name(id=name, ctx=ctx)

def new_ast_subscript(value, indices):
    if len(indices) == 1:
        slice = indices[0]
    else:
        slice = ast.Tuple(elts=indices, ctx=ast.Load())
    return ast.Subscript(value=value, slice=slice)

def new_ast_assign(target, value):
    return ast.Assign(targets=[target], value=value, lineno=None)

def new_ast_list(elts):
    return ast.List(elts=elts, ctx=ast.Load())

def new_ast_add(left, right):
    return ast.BinOp(left=left, op=ast.Add(), right=right)

def deepcopy_ast_node(node, ctx=None):
    newnode = copy.deepcopy(node)
    newnode.ctx = ctx
    return newnode

def get_init_value_for_reduction(f):
    if f == 'max':
        return new_ast_const(-float('inf'))
    elif f == 'min':
        return new_ast_const(float('inf'))
    elif f == 'sum' or f == 'matmul':
        return new_ast_const(0)
    else:
        assert False