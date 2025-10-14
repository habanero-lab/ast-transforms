Introduction
============

A collection of AST-based transformations for Python.

This page provides a brief overview, installation instructions, and a simple usage example.

Installation
------------

.. code-block:: bash

    pip install ast-transforms

Usage Example
-------------

.. code-block:: python

    import ast
    import ast_transforms as at

    code = '''
    @mydecorator
    def foo():
        print("foo")
    '''

    # Parse code into an AST
    tree = ast.parse(code)

    # Apply the transformation
    tree = at.remove_func_decorator(tree)

    # Convert AST back to source code
    new_code = ast.unparse(tree)
    print(new_code)

Ouput
-----
.. code-block:: bash

    def foo():
        print("foo")

The list of AST transformation passes can be found in :doc:`API Documentation <api>`.
