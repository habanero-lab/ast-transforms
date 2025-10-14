A collection of AST-based transformations. Usage example:

```python
import ast
from ast_transforms import remove_func_decorator

code = '''
@mydecorator
def foo():
    print("foo")
'''

tree = ast.parse(code)
tree = remove_func_decorator(tree)  # removes all function decorators
newcode = ast.unparse(tree)
print(newcode)  # should print `def foo():\n    print("foo")`
```