import sympy
from sympy.matrices import Matrix, eye, zeros

# Top-level setup for potential witness objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism",
    "H_2: I is an ideal of R",
    "H_3: I is a subset of ker(f)",
    "¬Q: There does not exist a unique ring homomorphism f_bar: R/I -> S such that f(x) = f_bar(x + I)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    def get_attr(obj, name, default=None):
        if isinstance(obj, dict) and name in obj:
            return obj[name]
        elif hasattr(obj, name):
            return getattr(obj, name)
        return default

    def apply_f(x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    def call_op(op, x, y):
        if isinstance(op, dict):
            return op[(x, y)]
        return op(x, y)

    R = get_attr(witness, 'R', [])
    S = get_attr(witness, 'S', [])
    add_R = get_attr(witness, 'add_R')
    mul_R = get_attr(witness, 'mul_R')
    add_S = get_attr(witness, 'add_S')
    mul_S = get_attr(witness, 'mul_S')
    zero_R = get_attr(witness, 'zero_R')
    zero_S = get_attr(witness, 'zero_S')
    f = get_attr(witness, 'f')
    I = get_attr(witness, 'I', [])
    one_R = get_attr(witness, 'one_R')
    one_S = get_attr(witness, 'one_S')

    # H1: f is a ring homomorphism
    try:
        h1 = True
        for x in R:
            for y in R:
                if apply_f(call_op(add_R, x, y)) != call_op(add_S, apply_f(x), apply_f(y)):
                    h1 = False
                if apply_f(call_op(mul_R, x, y)) != call_op(mul_S, apply_f(x), apply_f(y)):
                    h1 = False
        if one_R is not None and one_S is not None:
            if apply_f(one_R) != one_S:
                h1 = False
    except Exception:
        h1 = False

    # H2: I is an ideal of R (left or right ideal)
    try:
        is_subgroup = True
        if zero_R not in I:
            is_subgroup = False
        else:
            for x in I:
                if x not in R:
                    is_subgroup = False
                    break
                has_inv = False
                for y in I:
                    if call_op(add_R, x, y) == zero_R and call_op(add_R, y, x) == zero_R:
                        has_inv = True
                        break
                if not has_inv:
                    is_subgroup = False
                    break
            if is_subgroup:
                for x in I:
                    for y in I:
                        if call_op(add_R, x, y) not in I:
                            is_subgroup = False
                            break
                        
        is_left = True
        is_right = True
        for r in R:
            for x in I:
                if call_op(mul_R, r, x) not in I:
                    is_left = False
                if call_op(mul_R, x, r) not in I:
                    is_right = False
                    
        h2 = is_subgroup and (is_left or is_right)
    except Exception:
        h2 = False

    # H3: I is a subset of ker(f)
    try:
        h3 = True
        for x in I:
            if apply_f(x) != zero_S:
                h3 = False
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails
    # The conclusion requires R/I to be a well-defined ring, which is true iff I is a two-sided ideal.
    # If I is only a one-sided ideal, R/I is not a ring, so no such ring homomorphism f_bar can exist.
    try:
        is_left = True
        is_right = True
        for r in R:
            for x in I:
                if call_op(mul_R, r, x) not in I:
                    is_left = False
                if call_op(mul_R, x, r) not in I:
                    is_right = False
        is_two_sided = is_left and is_right
        neg_q = not is_two_sided
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]