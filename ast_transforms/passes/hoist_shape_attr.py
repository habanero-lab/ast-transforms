import ast

class HoistShapeAttr(ast.NodeTransformer):
    '''
    Updates `a.shape[0]` to `a_shape_0` and inserts an assignment `a_shape_0 = a.shape[0]`
    before the loop.
    '''
    def __init__(self):
        self.hoisted_shapes_stack = []

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if (
            isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.attr == 'shape'
            and isinstance(node.slice, ast.Constant)
        ):
            array_name = node.value.value.id
            dim_index = node.slice.value
            new_name = f"{array_name}_shape_{dim_index}"
            tos = self.hoisted_shapes_stack[-1]
            if (array_name, dim_index) not in tos:
                tos.append((array_name, dim_index))            
            return ast.Name(id=new_name, ctx=ast.Load())
        else:
            return node

    def visit_For(self, node):
        self.hoisted_shapes_stack.append([])
        self.generic_visit(node)
        new_assignments = []
        for array_name, dim_index in self.hoisted_shapes_stack.pop():
            new_name = f"{array_name}_shape_{dim_index}"
            shape_access = ast.Subscript(
                value=ast.Attribute(
                    value=ast.Name(id=array_name, ctx=ast.Load()),
                    attr='shape',
                    ctx=ast.Load()
                ),
                slice=ast.Constant(value=dim_index),
                ctx=ast.Load()
            )
            assign = ast.Assign(
                targets=[ast.Name(id=new_name, ctx=ast.Store())],
                value=shape_access
            )
            new_assignments.append(assign)
        return new_assignments + [node]
    
def transform(tree):
    '''
    Transforms the AST by hoisting shape attribute accesses.
    '''
    tree = HoistShapeAttr().visit(tree)
    ast.fix_missing_locations(tree)
    return tree