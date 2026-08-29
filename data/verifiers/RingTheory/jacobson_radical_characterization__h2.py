import sympy
from sympy import QQ, ZZ, Poly, Symbol, Rational, Integer
from sympy.abc import x, y, z
import itertools
import math
import functools

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x \\in J(R)",
    "¬Q: There exists y \\in R such that 1 - xy is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Jacobson Radical Characterization conjecture.
    The witness can be a tuple (R, x) or (R, x, y).
    R is expected to be an object representing a ring, providing either:
      - .elements, .zero, .one, .add(a,b), .mul(a,b) for finite rings
      - .is_commutative_ring_with_identity, .is_in_J(x), .is_unit(a), .sub(a,b) for custom/infinite rings
    """
    try:
        if len(witness) == 3:
            R, x_val, y_counter = witness
            search_y = False
        elif len(witness) == 2:
            R, x_val = witness
            search_y = True
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def eq(a, b):
        if hasattr(R, 'eq'): return R.eq(a, b)
        return a == b

    # H_1: R is a commutative ring with identity
    h1 = False
    try:
        if hasattr(R, 'is_commutative_ring_with_identity'):
            if callable(R.is_commutative_ring_with_identity):
                h1 = R.is_commutative_ring_with_identity()
            else:
                h1 = bool(R.is_commutative_ring_with_identity)
        else:
            elements = R.elements
            zero = R.zero
            one = R.one
            
            is_comm_ring = True
            for a in elements:
                if not eq(R.add(a, zero), a): is_comm_ring = False; break
                if not eq(R.mul(a, one), a): is_comm_ring = False; break
                
                has_inv = False
                for b in elements:
                    if eq(R.add(a, b), zero):
                        has_inv = True
                        break
                if not has_inv: is_comm_ring = False; break
                
                for b in elements:
                    if not eq(R.add(a, b), R.add(b, a)): is_comm_ring = False; break
                    if not eq(R.mul(a, b), R.mul(b, a)): is_comm_ring = False; break
            
            if is_comm_ring:
                for a in elements:
                    for b in elements:
                        ab_add = R.add(a, b)
                        ab_mul = R.mul(a, b)
                        for c in elements:
                            if not eq(R.add(ab_add, c), R.add(a, R.add(b, c))): is_comm_ring = False; break
                            if not eq(R.mul(ab_mul, c), R.mul(a, R.mul(b, c))): is_comm_ring = False; break
                            if not eq(R.mul(a, R.add(b, c)), R.add(ab_mul, R.mul(a, c))): is_comm_ring = False; break
                        if not is_comm_ring: break
                    if not is_comm_ring: break
            h1 = is_comm_ring
    except Exception:
        h1 = False

    # H_2: x \in J(R)
    h2 = False
    try:
        if hasattr(R, 'is_in_J'):
            h2 = R.is_in_J(x_val)
        elif hasattr(R, 'J'):
            h2 = x_val in R.J()
        else:
            # Fallback for finite commutative rings: J(R) is the nilradical
            curr = x_val
            is_nilpotent = False
            for _ in range(len(R.elements)):
                if eq(curr, R.zero):
                    is_nilpotent = True
                    break
                curr = R.mul(curr, x_val)
            h2 = is_nilpotent
    except Exception:
        h2 = False

    # ¬Q: There exists y \in R such that 1 - xy is NOT a unit in R
    neg_q = False
    try:
        def is_unit(a):
            if hasattr(R, 'is_unit'): return R.is_unit(a)
            for b in R.elements:
                if eq(R.mul(a, b), R.one) and eq(R.mul(b, a), R.one):
                    return True
            return False
            
        def sub(a, b):
            if hasattr(R, 'sub'): return R.sub(a, b)
            for c in R.elements:
                if eq(R.add(b, c), R.zero):
                    return R.add(a, c)
            raise ValueError("No additive inverse found")

        if not search_y:
            xy = R.mul(x_val, y_counter)
            one_minus_xy = sub(R.one, xy)
            if not is_unit(one_minus_xy):
                neg_q = True
        else:
            for y_val in R.elements:
                xy = R.mul(x_val, y_val)
                one_minus_xy = sub(R.one, xy)
                if not is_unit(one_minus_xy):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]