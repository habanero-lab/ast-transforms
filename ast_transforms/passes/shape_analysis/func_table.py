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

def range(*args):
    '''
    The shape of range cannot be determined by the shape of its arguments.
    So simply return a None here, need another pass to pass the values of 
    the arguments.
    '''
    return None 

def slice(low, up, step):
    # ---- Validate inputs ----
    for name, arg in [("low", low), ("up", up), ("step", step)]:
        if not isinstance(arg, (int, type(None), str)):
            raise TypeError(f"{name} must be int, str, or None")

    step = 1 if step is None else step
    if step != 1:
        raise RuntimeError("Non-1 step is not supported in slice")

    low = 0 if low is None else low

    if isinstance(low, int) and low < 0:
        raise ValueError("Slice lower bound must be non-negative")

    # ---- Dispatch rules ----
    table = {
        (int, int): lambda low, up: (up - low,),
        (int, type(None)): lambda low, up: (None,) if low == 0 else (-low,),
        (int, str): lambda low, up: (f":{up}",) if low == 0 else (f"{low}:{up}",),
        (str, int): lambda low, up: (f"{low}:{up}",),
        (str, type(None)): lambda low, up: (f"{low}:",),
        (str, str): lambda low, up: (f"{low}:{up}",),
    }

    key = (type(low), type(up))
    if key not in table:
        raise NotImplementedError(f"Unsupported slice shape: low={low}, up={up}")

    return table[key](low, up)

def subscript(base, indices):
    shape = []
    for i, idx in enumerate(indices):
        # Case 1: scalar index
        if idx == ():
            pass
        elif len(idx) == 1:
            size = idx[0]
            # Case 2: non-negative integer index
            if isinstance(size, int) and size >= 0:
                shape.append(size)
            # Case 3: negative integer index
            elif isinstance(size, int) and size < 0:
                shape.append(base[i] + size)
            # Case 4: None index => full slice
            elif size is None:
                shape.append(base[i])
            # Case 5: symbolic index
            elif isinstance(size, str):
                shape.append(size)
            else:
                assert False, "Should not reach here"
        else:
            assert False, "Should not reach here"
    shape += base[len(indices):]
    return tuple(shape)

def numpy_sin(a):
    return uop_generic(a)

def numpy_cos(a):
    return uop_generic(a)

def numpy_tan(a):
    return uop_generic(a)

def numpy_arcsin(a):
    return uop_generic(a)

def numpy_asin(a):
    return uop_generic(a)

def numpy_arccos(a):
    return uop_generic(a)

def numpy_acos(a):
    return uop_generic(a)

def numpy_arctan(a):
    return uop_generic(a)

def numpy_atan(a):
    return uop_generic(a)

def numpy_sinh(a):
    return uop_generic(a)

def numpy_cosh(a):
    return uop_generic(a)

def numpy_tanh(a):
    return uop_generic(a)

def numpy_arcsinh(a):
    return uop_generic(a)

def numpy_asinh(a):
    return uop_generic(a)

def numpy_arccosh(a):
    return uop_generic(a)

def numpy_acosh(a):
    return uop_generic(a)

def numpy_arctanh(a):
    return uop_generic(a)

def numpy_atanh(a):
    return uop_generic(a)

def numpy_round(a, decimals=()):
    return uop_generic(a)

def numpy_rint(a):
    return uop_generic(a)

def numpy_log(a):
    return uop_generic(a)

def numpy_pow(a, b):
    assert len(b) == 0 or len(b) == 1 or len(b) == len(a)
    return a

def numpy_power(a, b):
    return numpy_pow(a, b)

def numpy_add(a, b):
    return binop_generic(a, b)


def pow(a, b):
    return numpy_pow(a, b)