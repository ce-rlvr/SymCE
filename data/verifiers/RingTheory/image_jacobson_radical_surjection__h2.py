import sympy
from sympy import eye, zeros
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Verifies that the witness is a valid counterexample to the false conjecture.
    The witness must provide:
      - R, S: iterables of elements in the rings
      - add_R, mul_R, zero_R, one_R: ring operations and identities for R
      - add_S, mul_S, zero_S, one_S: ring operations and identities for S
      - f: a function from R to S
      - J_R, J_S: iterables of elements in the Jacobson radicals of R and S
    """
    try:
        R = list(witness.R)
        S = list(witness.S)
        # Restrict to finite rings to ensure fast verification
        if len(R) > 100 or len(S) > 100:
            return [False, False, False]
            
        add_R = witness.add_R
        mul_R = witness.mul_R
        zero_R = witness.zero_R
        one_R = witness.one_R
        
        add_S = witness.add_S
        mul_S = witness.mul_S
        zero_S = witness.zero_S
        one_S = witness.one_S
        
        f = witness.f
        J_R = list(witness.J_R)
        J_S = list(witness.J_S)
    except Exception:
        return [False, False, False]

    def is_ring(elements, add, mul, zero, one):
        if zero not in elements or one not in elements: 
            return False
        
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False

        for a in elements:
            for b in elements:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                if ab_add not in elements: return False
                if ab_mul not in elements: return False
                if ab_add != add(b, a): return False
                
                for c in elements:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True

    def is_homomorphism(R_elems, S_elems, add_r, mul_r, one_r, add_s, mul_s, one_s, func):
        if func(one_r) != one_s: return False
        for a in R_elems:
            fa = func(a)
            if fa not in S_elems: return False
            for b in R_elems:
                if func(add_r(a, b)) != add_s(fa, func(b)): return False
                if func(mul_r(a, b)) != mul_s(fa, func(b)): return False
        return True

    try:
        h1 = is_ring(R, add_R, mul_R, zero_R, one_R) and \
             is_ring(S, add_S, mul_S, zero_S, one_S) and \
             is_homomorphism(R, S, add_R, mul_R, one_R, add_S, mul_S, one_S, f)
    except Exception:
        h1 = False

    def is_unit(elements, mul, one, a):
        for b in elements:
            if mul(a, b) == one and mul(b, a) == one:
                return True
        return False

    def is_jacobson_radical(elements, add, mul, zero, one, J):
        for x in J:
            if x not in elements: return False
            
        def neg_elem(a):
            for b in elements:
                if add(a, b) == zero: return b
            return None
            
        actual_J = []
        for x in elements:
            in_J = True
            for y in elements:
                xy = mul(x, y)
                minus_xy = neg_elem(xy)
                one_minus_xy = add(one, minus_xy)
                if not is_unit(elements, mul, one, one_minus_xy):
                    in_J = False
                    break
            if in_J:
                actual_J.append(x)
                
        for a in J:
            if a not in actual_J: return False
        for b in actual_J:
            if b not in J: return False
        return True

    try:
        h2 = is_jacobson_radical(R, add_R, mul_R, zero_R, one_R, J_R) and \
             is_jacobson_radical(S, add_S, mul_S, zero_S, one_S, J_S)
    except Exception:
        h2 = False

    try:
        neg_q = False
        for x in J_R:
            if f(x) not in J_S:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings and f is a homomorphism from R to S",
    "H_2: J(R) and J(S) are the Jacobson radicals of R and S",
    "¬Q: The image f(J(R)) is not contained in J(S)"
]

N_HYP = 2
NEG_Q_INDEX = 2