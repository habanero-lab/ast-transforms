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
    if not (len(left) > 0 and len(right) > 0):
        raise RuntimeError("Matmul cannot happen on scalar operands")

    if left[-1] != right[0]:
        raise RuntimeError(f"Mismatched contracting dimension found for matmul: {left[-1]} and {right[0]}")
    return left[:-1] + right[1:]

def numpy_pow(a, b):
    assert len(b) == 0 or len(b) == 1 or len(b) == len(a)
    return a

def numpy_power(a, b):
    return numpy_pow(a, b)

def numpy_add(a, b):
    return binop_generic(a, b)


def pow(a, b):
    return numpy_pow(a, b)