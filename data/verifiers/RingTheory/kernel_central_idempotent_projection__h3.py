import sympy
from sympy import eye, zeros
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: e is a central idempotent element of R",
    "¬Q: The map f is not a surjective ring homomorphism with kernel equal to the ideal (1-e)R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Extract witness
    try:
        if isinstance(witness, dict):
            R = witness['R']
            e = witness['e']
            f = witness['f']
            add = witness.get('add', lambda x, y: x + y)
            mul = witness.get('mul', lambda x, y: x * y)
            eq = witness.get('eq', lambda x, y: x == y)
            zero = witness.get('zero', None)
            one = witness.get('one', None)
            S = witness.get('S', None)
            add_S = witness.get('add_S', add)
            mul_S = witness.get('mul_S', mul)
            eq_S = witness.get('eq_S', eq)
            zero_S = witness.get('zero_S', None)
            one_S = witness.get('one_S', None)
        else:
            R, e, f = witness
            add = lambda x, y: x + y
            mul = lambda x, y: x * y
            eq = lambda x, y: x == y
            zero = None
            one = None
            S = None
            add_S = add
            mul_S = mul
            eq_S = eq
            zero_S = None
            one_S = None
            
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
    except Exception:
        return [False, False, False]

    # Find zero and one if not provided
    try:
        if zero is None:
            for x in R:
                if all(eq(add(x, y), y) and eq(add(y, x), y) for y in R):
                    zero = x
                    break
        if one is None:
            for x in R:
                if all(eq(mul(x, y), y) and eq(mul(y, x), y) for y in R):
                    one = x
                    break
    except Exception:
        pass

    # H1: R is a ring
    h1 = False
    try:
        if isinstance(R, (list, tuple)) and zero is not None and one is not None:
            h1 = True
            for x in R:
                has_inv = False
                for y in R:
                    if eq(add(x, y), zero) and eq(add(y, x), zero):
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                for y in R:
                    if not any(eq(add(x, y), z) for z in R): h1 = False
                    if not any(eq(mul(x, y), z) for z in R): h1 = False
                    if not eq(add(x, y), add(y, x)): h1 = False
                    for z in R:
                        if not eq(add(add(x, y), z), add(x, add(y, z))): h1 = False
                        if not eq(mul(mul(x, y), z), mul(x, mul(y, z))): h1 = False
                        if not eq(mul(x, add(y, z)), add(mul(x, y), mul(x, z))): h1 = False
                        if not eq(mul(add(x, y), z), add(mul(x, z), mul(y, z))): h1 = False
                if not h1: break
    except Exception:
        h1 = False

    # H2: e is a central idempotent element of R
    h2 = False
    try:
        if any(eq(e, x) for x in R) and eq(mul(e, e), e):
            h2 = True
            for x in R:
                if not eq(mul(e, x), mul(x, e)):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The map f is not a surjective ring homomorphism with kernel equal to the ideal (1-e)R
    neg_q = False
    try:
        is_surjective = True
        if S is None:
            S_list = []
            for x in R:
                fx = f_func(x)
                if not any(eq_S(fx, y) for y in S_list):
                    S_list.append(fx)
        else:
            S_list = S
            for y in S_list:
                if not any(eq_S(f_func(x), y) for x in R):
                    is_surjective = False
                    break
                    
        if zero_S is None:
            for x in S_list:
                if all(eq_S(add_S(x, y), y) and eq_S(add_S(y, x), y) for y in S_list):
                    zero_S = x
                    break
        if one_S is None:
            for x in S_list:
                if all(eq_S(mul_S(x, y), y) and eq_S(mul_S(y, x), y) for y in S_list):
                    one_S = x
                    break
                    
        is_hom = True
        if not is_surjective:
            is_hom = False
        elif S is not None:
            for x in R:
                if not any(eq_S(f_func(x), y) for y in S_list):
                    is_hom = False
                    break
                    
        if is_hom:
            if zero_S is None or one_S is None or one is None:
                is_hom = False
            elif not eq_S(f_func(one), one_S):
                is_hom = False
            else:
                for x in R:
                    for y in R:
                        if not eq_S(f_func(add(x, y)), add_S(f_func(x), f_func(y))):
                            is_hom = False
                            break
                        if not eq_S(f_func(mul(x, y)), mul_S(f_func(x), f_func(y))):
                            is_hom = False
                            break
                    if not is_hom: break
                
        ker_f = []
        if zero_S is not None:
            for x in R:
                if eq_S(f_func(x), zero_S):
                    ker_f.append(x)
                    
        neg_e = None
        for x in R:
            if eq(add(e, x), zero):
                neg_e = x
                break
                
        if neg_e is None or one is None:
            kernel_equals_ideal = False
        else:
            one_minus_e = add(one, neg_e)
            ideal = []
            for x in R:
                elem = mul(one_minus_e, x)
                if not any(eq(elem, y) for y in ideal):
                    ideal.append(elem)
                    
            kernel_equals_ideal = True
            for a in ker_f:
                if not any(eq(a, b) for b in ideal):
                    kernel_equals_ideal = False
                    break
            if kernel_equals_ideal:
                for b in ideal:
                    if not any(eq(a, b) for a in ker_f):
                        kernel_equals_ideal = False
                        break
                        
        q = is_hom and kernel_equals_ideal
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]