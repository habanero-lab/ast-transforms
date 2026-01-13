import ast

class AddFuncDecorator(ast.NodeTransformer):
    def __init__(self, decorator: str):
        if decorator.startswith('@'):
            decorator = decorator[1:]
        self.decorator = decorator

    def visit_FunctionDef(self, node):
        dec_node = ast.parse(self.decorator).body[0]
        assert isinstance(dec_node, ast.Expr)
        node.decorator_list.append(dec_node.value)
        return node

def transform(node, decorator):
    return AddFuncDecorator(decorator).visit(node)
