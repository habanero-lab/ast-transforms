import ast
from . import func_table

class AttachShapes(ast.NodeVisitor):
    def __init__(self, rt_vals):
        self.node_shapes = {}
        self.var_shapes = {}
        self.init_rt_var_shapes(rt_vals)

    def init_rt_var_shapes(self, rt_vals):
        for var, val in rt_vals.items():
            if isinstance(val, (int, float, bool)):
                self.var_shapes[var] = ()
            elif hasattr(val, 'shape'):
                self.var_shapes[var] = val.shape
            else:
                self.var_shapes[var] = None  # otherwise shape is undefined

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float, bool)):
            self.node_shapes[node] = ()
        else:
            self.node_shapes[node] = None  # otherwise shape is undefined

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.node_shapes[node] = self.var_shapes[node.id]
        else:
            raise NotImplementedError
        
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv)):
            f = getattr(func_table, 'binop_generic')
            self.node_shapes[node] = f(self.node_shapes[node.left], self.node_shapes[node.right])
        elif isinstance(node.op, ast.MatMult):
            f = getattr(func_table, 'matmul_generic')
            self.node_shapes[node] = f(self.node_shapes[node.left], self.node_shapes[node.right])


def visit(tree, rt_vals):
    visitor = AttachShapes(rt_vals)
    visitor.visit(tree)
    return visitor.node_shapes