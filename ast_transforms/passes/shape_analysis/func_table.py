def binop_generic(left, right):
    if left == right:
        return left
    elif left == ():
        return right
    elif right == ():
        return left
    else:
        raise NotImplementedError("Shape broadcasting is not implemented")
    
def matmul_generic(left, right):
    assert len(left) > 0 and len(right) > 0
    left, right = list(left), list(right)
    a, b = left.pop(), right.pop(0)
    assert a == b, f"The contracting dimension must be the same for matmul, got {a} and {b}"
    return tuple(left + right)

def numpy_add(a, b):
    return binop_generic(a, b)
