def uop_generic(a):
    return a

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

def numpy_pow(a, b):
    assert len(b) == 0 or len(b) == 1 or len(b) == len(a)
    return a

def numpy_power(a, b):
    return numpy_pow(a, b)

def pow(a, b):
    return numpy_pow(a, b)

def numpy_add(a, b):
    return binop_generic(a, b)
