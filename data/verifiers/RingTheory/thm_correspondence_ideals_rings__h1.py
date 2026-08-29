import itertools
import functools
import math
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        def get_attr(w, name):
            if isinstance(w, dict):
                return w[name]
            else:
                return getattr(w, name)

        R_raw = get_attr(witness, 'R')
        S_raw = get_attr(witness, 'S')
        R = list(set(R_raw))
        S = list(set(S_raw))
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        f_map = get_attr(witness, 'f')
        K = set(get_attr(witness, 'K'))
    except Exception:
        return [False, False, False]

    if len(R) > 15 or len(S) > 15:
        return [False, False, False]

    def eval_op(op, a, b):
        if isinstance(op, dict):
            return op[(a, b)]
        else:
            return op(a, b)

    def eval_f(op, a):
        if isinstance(op, dict):
            return op[a]
        else:
            return op(a)

    # Find zero of S
    zero_S = None
    for z_cand in S:
        try:
            if all(eval_op(add_S, a, z_cand) == a for a in S) and all(eval_op(add_S, z_cand, a) == a for a in S):
                zero_S = z_cand
                break
        except Exception:
            pass
            
    # Find zero of R
    zero_R = None
    for z_cand in R:
        try:
            if all(eval_op(add_R, a, z_cand) == a for a in R) and all(eval_op(add_R, z_cand, a) == a for a in R):
                zero_R = z_cand
                break
        except Exception:
            pass

    def is_ring(elements, add, mul, zero):
        if zero not in elements: return False
        for a in elements:
            for b in elements:
                if eval_op(add, a, b) not in elements: return False
                if eval_op(add, a, b) != eval_op(add, b, a): return False
                for c in elements:
                    if eval_op(add, eval_op(add, a, b), c) != eval_op(add, a, eval_op(add, b, c)): return False
        for a in elements:
            if eval_op(add, a, zero) != a: return False
        for a in elements:
            has_inv = False
            for b in elements:
                if eval_op(add, a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
        for a in elements:
            for b in elements:
                if eval_op(mul, a, b) not in elements: return False
                for c in elements:
                    if eval_op(mul, eval_op(mul, a, b), c) != eval_op(mul, a, eval_op(mul, b, c)): return False
        for a in elements:
            for b in elements:
                for c in elements:
                    if eval_op(mul, a, eval_op(add, b, c)) != eval_op(add, eval_op(mul, a, b), eval_op(mul, a, c)): return False
                    if eval_op(mul, eval_op(add, a, b), c) != eval_op(add, eval_op(mul, a, c), eval_op(mul, b, c)): return False
        return True

    # H1: f is a surjective ring homomorphism
    try:
        h1 = True
        if zero_R is None or zero_S is None:
            h1 = False
        elif not is_ring(R, add_R, mul_R, zero_R):
            h1 = False
        elif not is_ring(S, add_S, mul_S, zero_S):
            h1 = False
        
        if h1:
            f_image = set()
            for a in R:
                f_a = eval_f(f_map, a)
                if f_a not in S:
                    h1 = False
                    break
                f_image.add(f_a)
            if h1 and f_image != set(S):
                h1 = False
        
        if h1:
            for a in R:
                for b in R:
                    f_a = eval_f(f_map, a)
                    f_b = eval_f(f_map, b)
                    ab_add = eval_op(add_R, a, b)
                    ab_mul = eval_op(mul_R, a, b)
                    if eval_f(f_map, ab_add) != eval_op(add_S, f_a, f_b):
                        h1 = False
                        break
                    if eval_f(f_map, ab_mul) != eval_op(mul_S, f_a, f_b):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: K is the kernel of f
    try:
        if zero_S is None:
            h2 = False
        else:
            actual_ker = set(a for a in R if eval_f(f_map, a) == zero_S)
            h2 = (K == actual_ker)
    except Exception:
        h2 = False

    # neg_Q: The map I -> f(I) is NOT a bijection from ideals of R containing K to ideals of S
    try:
        def get_ideals(elements, add, mul, zero):
            if zero is None:
                return []
            ideals = []
            n = len(elements)
            for r in range(1, n + 1):
                for subset in itertools.combinations(elements, r):
                    subset = set(subset)
                    if zero not in subset:
                        continue
                    is_ideal = True
                    for a in subset:
                        for b in subset:
                            if eval_op(add, a, b) not in subset:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                    if not is_ideal:
                        continue
                    for a in subset:
                        for r_elem in elements:
                            if eval_op(mul, a, r_elem) not in subset:
                                is_ideal = False
                                break
                            if eval_op(mul, r_elem, a) not in subset:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                    if is_ideal:
                        ideals.append(frozenset(subset))
            return ideals

        ideals_R = get_ideals(R, add_R, mul_R, zero_R)
        ideals_S = get_ideals(S, add_S, mul_S, zero_S)

        ideals_R_K = [I for I in ideals_R if K.issubset(I)]

        is_bijection = True
        mapped_ideals = []
        for I in ideals_R_K:
            f_I = frozenset(eval_f(f_map, a) for a in I)
            if f_I not in ideals_S:
                is_bijection = False
                break
            mapped_ideals.append(f_I)
        
        if is_bijection:
            if len(set(mapped_ideals)) != len(ideals_R_K):
                is_bijection = False
            elif set(mapped_ideals) != set(ideals_S):
                is_bijection = False
        
        neg_q = not is_bijection

    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism",
    "H_2: K is the kernel of f",
    "¬Q: The map I -> f(I) is not a bijection from the set of ideals of R containing K to the set of ideals of S"
]

N_HYP = 2
NEG_Q_INDEX = 2