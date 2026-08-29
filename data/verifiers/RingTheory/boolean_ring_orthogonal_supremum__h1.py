import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            get_add = witness['add']
            get_mul = witness['mul']
            x_val = witness['x']
            y_val = witness['y']
            if not callable(get_add):
                add_dict = get_add
                get_add = lambda a, b: add_dict[(a, b)]
            if not callable(get_mul):
                mul_dict = get_mul
                get_mul = lambda a, b: mul_dict[(a, b)]
        elif hasattr(witness, 'elements'):
            elements = witness.elements
            get_add = witness.add
            get_mul = witness.mul
            x_val = witness.x
            y_val = witness.y
        elif isinstance(witness, tuple) and len(witness) == 5:
            if isinstance(witness[0], int):
                n, add_table, mul_table, x_val, y_val = witness
                elements = list(range(n))
                get_add = lambda a, b: add_table[a][b]
                get_mul = lambda a, b: mul_table[a][b]
            else:
                elements, add_func, mul_func, x_val, y_val = witness
                get_add = add_func
                get_mul = mul_func
        else:
            return [False, False, False]
            
        elements = list(elements)
    except Exception:
        return [False, False, False]

    try:
        # H1: R is a ring
        h1 = True
        if not elements:
            h1 = False
            
        if h1:
            for a in elements:
                for b in elements:
                    add_ab = get_add(a, b)
                    mul_ab = get_mul(a, b)
                    if not any(bool(add_ab == e) for e in elements):
                        h1 = False
                        break
                    if not any(bool(mul_ab == e) for e in elements):
                        h1 = False
                        break
                if not h1: break

        zero = None
        if h1:
            for e in elements:
                is_zero = True
                for a in elements:
                    if not bool(get_add(e, a) == a) or not bool(get_add(a, e) == a):
                        is_zero = False
                        break
                if is_zero:
                    zero = e
                    break
            if zero is None:
                h1 = False
                
        if h1:
            for a in elements:
                has_inv = False
                for b in elements:
                    if bool(get_add(a, b) == zero) and bool(get_add(b, a) == zero):
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                    
        if h1:
            for a in elements:
                for b in elements:
                    if not bool(get_add(a, b) == get_add(b, a)):
                        h1 = False
                        break
                if not h1: break
                
        if h1:
            for a in elements:
                for b in elements:
                    for c in elements:
                        if not bool(get_add(a, get_add(b, c)) == get_add(get_add(a, b), c)):
                            h1 = False
                        if not bool(get_mul(a, get_mul(b, c)) == get_mul(get_mul(a, b), c)):
                            h1 = False
                        if not bool(get_mul(a, get_add(b, c)) == get_add(get_mul(a, b), get_mul(a, c))):
                            h1 = False
                        if not bool(get_mul(get_add(a, b), c) == get_add(get_mul(a, c), get_mul(b, c))):
                            h1 = False
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    try:
        if h1:
            x_in = any(bool(x_val == e) for e in elements)
            y_in = any(bool(y_val == e) for e in elements)
            h2 = x_in and y_in and bool(get_mul(x_val, y_val) == zero)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            def leq(a, b):
                return bool(get_mul(a, b) == a)
            
            x_plus_y = get_add(x_val, y_val)
            
            is_ub = leq(x_val, x_plus_y) and leq(y_val, x_plus_y)
            
            is_least = True
            for z_elem in elements:
                if leq(x_val, z_elem) and leq(y_val, z_elem):
                    if not leq(x_plus_y, z_elem):
                        is_least = False
                        break
            
            q = is_ub and is_least
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring and <= is defined by a <= b iff ab = a",
    "H_2: x and y are elements of R such that xy = 0",
    "¬Q: x+y is not the supremum of x and y with respect to <="
]

N_HYP = 2
NEG_Q_INDEX = 2