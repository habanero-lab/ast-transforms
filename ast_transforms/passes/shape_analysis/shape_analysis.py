import ast

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
        self.node_shapes[node] = ()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.node_shapes[node] = self.var_shapes[node.id]
        else:
            raise NotImplementedError


def visit(tree, rt_vals):
    visitor = AttachShapes(rt_vals)
    visitor.visit(tree)
    return visitor.node_shapes