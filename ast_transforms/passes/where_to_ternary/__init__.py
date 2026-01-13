import ast

class WhereToTernary(ast.NodeTransformer):
    def visit_Call(self, node):
        func = node.func
        if (
            (isinstance(func, ast.Name) and func.id == 'where')
            or 
            (isinstance(func, ast.Attribute)
             and isinstance(func.value, ast.Name)
             and func.attr == 'where'
             and func.value.id in ['np', 'numpy', 'torch', 'cupy'])
        ):
            assert len(node.args) == 3, f"where should have 3 arguments, but got {len(node.args)}"
            return ast.IfExp(
                test=node.args[0],
                body=node.args[1],
                orelse=node.args[2],
                lineno=node.lineno
            )
        return node

def transform(node):
    return WhereToTernary().visit(node)