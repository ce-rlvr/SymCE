import sympy
from sympy.matrices import eye, zeros
import itertools
import functools

# Standard ring/matrix objects that might be used in a witness
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: I and J are ideals of R",
    "H_3: I and J are comaximal in R",
    "¬Q: f(I) and f(J) are not comaximal in S"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Expects a witness object or dictionary with the following attributes/keys:
      - R, S: iterables representing the elements of the rings
      - add_R, mul_R: callables for operations in R, e.g., add_R(a, b)
      - add_S, mul_S: callables for operations in S
      - f: callable representing the map from R to S
      - I, J: iterables representing the ideals in R
    """
    if isinstance(witness, dict):
        class Dummy: pass
        w = Dummy()
        w.__dict__.update(witness)
        witness = w

    try:
        R = list(witness.R)
        S = list(witness.S)
        add_R = witness.add_R
        mul_R = witness.mul_R
        add_S = witness.add_S
        mul_S = witness.mul_S
        f = witness.f
        I = list(witness.I)
        J = list(witness.J)
    except Exception:
        return [False, False, False, False]

    def unique(lst):
        res = []
        for x in lst:
            if x not in res:
                res.append(x)
        return res

    def set_eq(l1, l2):
        for x in l1:
            if x not in l2: return False
        for x in l2:
            if x not in l1: return False
        return True

    def is_ideal(K, ring, add, mul):
        if not K: return False
        # Must be a subset
        for x in K:
            if x not in ring:
                return False
        # Closed under addition
        for x in K:
            for y in K:
                if add(x, y) not in K:
                    return False
        # Contains zero
        zeros_ring = [z for z in ring if all(add(z, x) == x for x in ring)]
        if not zeros_ring: return False
        zero = zeros_ring[0]
        if zero not in K: return False
        # Absorbs multiplication from ring
        for x in K:
            for r in ring:
                if mul(r, x) not in K:
                    return False
                if mul(x, r) not in K:
                    return False
        return True

    def get_identity(ring, mul):
        for e in ring:
            if all(mul(e, x) == x and mul(x, e) == x for x in ring):
                return e
        return None

    # H_1: f is a surjective ring homomorphism from R to S
    h1 = True
    try:
        f_R = unique([f(x) for x in R])
        if not set_eq(f_R, S):
            h1 = False
            
        for x in R:
            for y in R:
                if f(add_R(x, y)) != add_S(f(x), f(y)):
                    h1 = False
                if f(mul_R(x, y)) != mul_S(f(x), f(y)):
                    h1 = False
                    
        id_R = get_identity(R, mul_R)
        id_S = get_identity(S, mul_S)
        if id_R is not None and id_S is not None:
            if f(id_R) != id_S:
                h1 = False
        elif id_R is None or id_S is None:
            # We require rings to have an identity for comaximality to be well-behaved
            h1 = False
    except Exception:
        h1 = False

    # H_2: I and J are ideals of R
    try:
        h2 = is_ideal(I, R, add_R, mul_R) and is_ideal(J, R, add_R, mul_R)
    except Exception:
        h2 = False

    # H_3: I and J are comaximal in R (proper ideals whose sum is R)
    try:
        if set_eq(I, R) or set_eq(J, R):
            h3 = False
        else:
            sum_IJ = unique([add_R(x, y) for x in I for y in J])
            h3 = set_eq(sum_IJ, R)
    except Exception:
        h3 = False

    # ¬Q: f(I) and f(J) are NOT comaximal in S
    try:
        f_I = unique([f(x) for x in I])
        f_J = unique([f(x) for x in J])
        
        is_proper_fI = not set_eq(f_I, S)
        is_proper_fJ = not set_eq(f_J, S)
        sum_fIfJ = unique([add_S(x, y) for x in f_I for y in f_J])
        is_sum_S = set_eq(sum_fIfJ, S)
        
        comaximal_in_S = is_proper_fI and is_proper_fJ and is_sum_S
        neg_q = not comaximal_in_S
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]