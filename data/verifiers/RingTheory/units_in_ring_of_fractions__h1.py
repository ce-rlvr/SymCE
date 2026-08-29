import sympy
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
import math
import itertools
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x = Symbol('x')
y = Symbol('y')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    "If S is a multiplicatively closed subset of R, 1 in S, and s in S, 
    then s/1 is a unit in the ring of fractions S^(-1)R."
    """
    # Extract witness components
    try:
        R, S, s = witness
    except Exception:
        try:
            R = witness['R']
            S = witness['S']
            s = witness['s']
        except Exception:
            try:
                R = witness.R
                S = witness.S
                s = witness.s
            except Exception:
                return [False, False, False, False]

    # Robust equality check
    def eq(a, b):
        try:
            res = (a == b)
            if isinstance(res, bool):
                if res: return True
            else:
                if res.all(): return True
        except Exception:
            pass
        try:
            if (a - b) == 0: return True
        except Exception:
            pass
        try:
            if (a - b).is_zero_matrix: return True
        except Exception:
            pass
        return False

    # H1: S is a multiplicatively closed subset of R
    try:
        is_subset = True
        for elem in S:
            if not any(eq(elem, y_elem) for y_elem in R):
                is_subset = False
                break
        
        is_mult_closed = True
        for x_elem in S:
            for y_elem in S:
                try:
                    xy = x_elem * y_elem
                    if not any(eq(xy, z) for z in S):
                        is_mult_closed = False
                        break
                except Exception:
                    is_mult_closed = False
                    break
            if not is_mult_closed:
                break
        h1 = is_subset and is_mult_closed
    except Exception:
        h1 = False

    # H2: 1 is in S
    try:
        identities = []
        for e in R:
            is_id = True
            for x_elem in R:
                try:
                    if not (eq(e * x_elem, x_elem) and eq(x_elem * e, x_elem)):
                        is_id = False
                        break
                except Exception:
                    is_id = False
                    break
            if is_id:
                identities.append(e)
        
        h2 = False
        for e in identities:
            if any(eq(e, x_elem) for x_elem in S):
                h2 = True
                break
    except Exception:
        h2 = False

    # H3: s is an element of S
    try:
        h3 = any(eq(s, x_elem) for x_elem in S)
    except Exception:
        h3 = False

    # Find additive identity (zero) for reversibility checks
    try:
        zeros_list = []
        for z in R:
            is_z = True
            for x_elem in R:
                try:
                    if not (eq(z + x_elem, x_elem) and eq(x_elem + z, x_elem)):
                        is_z = False
                        break
                except Exception:
                    is_z = False
                    break
            if is_z:
                zeros_list.append(z)
        zero = zeros_list[0] if zeros_list else None
    except Exception:
        zero = None

    # Helper to evaluate if s/1 is a unit in S^(-1)R
    def is_unit_in_fractions(R, S, s, zero):
        # 1. Check if the left ring of fractions S^(-1)R exists
        # Left Ore condition
        left_ore = True
        for r in R:
            for t in S:
                if not any(eq(t_prime * r, r_prime * t) for r_prime in R for t_prime in S):
                    left_ore = False
                    break
            if not left_ore:
                break
                
        # Left reversibility
        left_reversible = True
        if zero is not None:
            for r in R:
                for t in S:
                    if eq(r * t, zero):
                        if not any(eq(t_prime * r, zero) for t_prime in S):
                            left_reversible = False
                            break
                if not left_reversible:
                    break
                    
        if not (left_ore and left_reversible):
            return False  # Ring of fractions does not exist
            
        # 2. Check if R is commutative
        is_comm = True
        for x_elem in R:
            for y_elem in R:
                if not eq(x_elem * y_elem, y_elem * x_elem):
                    is_comm = False
                    break
            if not is_comm:
                break
                
        # 3. Evaluate unit condition
        if is_comm:
            # In a commutative ring, s/1 is a unit iff there exists r/t such that u(sr - t) = 0
            for r in R:
                for t in S:
                    for u in S:
                        if eq((u * s) * r, u * t):
                            return True
            return False
        else:
            # In a non-commutative ring, search for a two-sided inverse t^{-1} r
            for r in R:
                for t in S:
                    # Check if t^{-1} r is a right inverse of 1^{-1} s
                    right_inv = False
                    for t3 in S:
                        for r3 in R:
                            if eq(t3 * s, r3 * t):
                                for u1 in R:
                                    u1_t3 = u1 * t3
                                    if any(eq(u1_t3, x_elem) for x_elem in S):
                                        if eq(u1_t3, (u1 * r3) * r):
                                            right_inv = True
                                            break
                            if right_inv:
                                break
                        if right_inv:
                            break
                    if not right_inv:
                        continue
                        
                    # Check if t^{-1} r is a left inverse of 1^{-1} s
                    left_inv = False
                    for t4 in S:
                        den = t4 * t
                        num = (t4 * r) * s
                        for v1 in R:
                            v1_den = v1 * den
                            if any(eq(v1_den, x_elem) for x_elem in S):
                                if eq(v1_den, v1 * num):
                                    left_inv = True
                                    break
                        if left_inv:
                            break
                            
                    if right_inv and left_inv:
                        return True
            return False

    # neg_Q: s/1 is NOT a unit in S^(-1)R
    try:
        neg_q = not is_unit_in_fractions(R, S, s, zero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 1 is in S",
    "H_3: s is an element of S",
    "¬Q: The fraction s/1 is not a unit in the ring of fractions S^(-1)R"
]

N_HYP = 3
NEG_Q_INDEX = 3