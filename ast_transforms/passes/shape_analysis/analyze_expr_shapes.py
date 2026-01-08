import ast
import inspect
from . import func_table

class AnalyzeExprShapes(ast.NodeVisitor):
    def __init__(self, rt_vals):
        self.node_shapes = {}
        self.var_shapes = {}
        self.modules = {}
        self.init_rt_var_shapes(rt_vals)
        self.init_module_names(rt_vals)

    def init_rt_var_shapes(self, rt_vals):
        for var, val in rt_vals.items():
            if isinstance(val, (int, float, bool)):
                self.var_shapes[var] = ()
            elif hasattr(val, 'shape'):
                self.var_shapes[var] = val.shape
            else:
                self.var_shapes[var] = None  # otherwise shape is undefined

    def init_module_names(self, rt_vals):
        for var, val in rt_vals.items():
            if inspect.ismodule(val):
                self.modules[var] = val

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float, bool)):
            self.node_shapes[node] = ()
        else:
            self.node_shapes[node] = None  # otherwise shape is undefined

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in self.var_shapes:
                self.node_shapes[node] = self.var_shapes[node.id]
            else:
                raise RuntimeError
        else:
            raise RuntimeError
        
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv)):
            f = getattr(func_table, 'binop_generic')
            self.node_shapes[node] = f(self.node_shapes[node.left], self.node_shapes[node.right])
        elif isinstance(node.op, ast.MatMult):
            f = getattr(func_table, 'matmul_generic')
            self.node_shapes[node] = f(self.node_shapes[node.left], self.node_shapes[node.right])
        else:
            raise NotImplementedError
        
    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)

        if isinstance(node.func, ast.Name):
            f = getattr(func_table, node.func.id)
        elif isinstance(node.func, ast.Attribute):
            assert isinstance(node.func.value, ast.Name), \
                "Function calls only suport named calls or named module calls"            
            assert node.func.value.id in self.modules
            module_name = self.modules[node.func.value.id].__name__
            f = getattr(func_table, f"{module_name}_{node.func.attr}")
        else:
            assert False, "Impossible path"

        self.node_shapes[node] = f(*[self.node_shapes[arg] for arg in node.args])


def visit(tree, rt_vals):
    visitor = AnalyzeExprShapes(rt_vals)
    visitor.visit(tree)
    return visitor.node_shapes