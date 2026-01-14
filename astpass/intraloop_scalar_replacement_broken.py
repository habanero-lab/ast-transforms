import ast
from astpass.utils import *

class ArrayReferenceCheck(ast.NodeVisitor):
    def __init__(self):
        self.array_indices = {}
        self.array_referenced_times = {}
        self.array_ever_written = {}
        self.always_same_index = {}

    def visit_Subscript(self, node):
        
        if isinstance(node.value, ast.Name):
            dump(node)
            name = node.value.id
            self.array_referenced_times[name] = self.array_referenced_times.get(name, 0) + 1
            if name not in self.array_ever_written:
                self.array_ever_written[name] = False

            # Check if the array is always referenced with the same index
            if name not in self.array_indices:
                self.array_indices[name] = ast.unparse(node.slice)
                self.always_same_index[name] = True
            else:
                if self.array_indices[name] != ast.unparse(node.slice):
                    self.always_same_index[name] = False

            if isinstance(node.ctx, ast.Store):
                self.array_ever_written[name] = True
            
        return node


class IntraloopScalarReplacement(ast.NodeTransformer):
    def visit_For(self, node):
        self.generic_visit(node)

        visitor = ArrayReferenceCheck()
        visitor.visit(node)

        scalar_count = 0
     
        for varname in visitor.always_same_index:
            indices = visitor.array_indices[varname]
            # Only perform the replacement if this condition is met
            if visitor.always_same_index[varname] and visitor.array_referenced_times[varname] > 0:
                scalar_var = f'__scalar_{scalar_count}'
                ReplaceSubscriptsWithName(varname, indices, scalar_var).visit(node)
                scalar_count += 1

                # Insert the stores at the end of the loop if the array is ever written to
                if visitor.array_ever_written[varname]:
                    node.body.append(
                        new_ast_assign_from_str(f'{varname}[{indices}] = {scalar_var}')
                    )

        # # Scan the loop body and replace the subscripts with the generated scalar variables
        # for i, sub in enumerate(candidates):
        #     scalar_var = f'__scalar_{i}'
        #     ReplaceSubscriptsWithName(sub, scalar_var).visit(node)

        # # Insert the stores at the end of the loop
        # for i, sub in enumerate(candidates):
        #     scalar_var = f'__scalar_{i}'
        #     node.body.append(
        #         new_ast_assign(
        #             deepcopy_ast_node(sub, ctx=ast.Store()),
        #             new_ast_name(scalar_var)
        #         )
        #     )

        return node

class ReplaceSubscriptsWithName(ast.NodeTransformer):
    def __init__(self, name, indices, scalar_var):
        self.name = name
        self.indices = indices
        self.scalar_var = scalar_var

    def visit_Subscript(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == self.name and ast.unparse(node.slice) == self.indices:
            if isinstance(node.ctx, ast.Load):
                return new_ast_name(self.scalar_var)
            else:
                return new_ast_name(self.scalar_var, ctx=ast.Store())
        return node

def transform(node):
    return IntraloopScalarReplacement().visit(node)