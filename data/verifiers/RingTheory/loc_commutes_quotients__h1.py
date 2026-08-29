import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import itertools
import functools
import math

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "Localization Commutes with Quotients" for non-commutative rings.
    """
    try:
        R = witness['R']
        S = witness['S']
        I = witness['I']
    except Exception:
        return [False, False, False, False]

    class RingWrapper:
        def __init__(self, R, S, I, witness):
            self.R = R
            self.S = S
            self.I = I
            self._add = witness.get('add')
            self._mul = witness.get('mul')
            
        def add(self, a, b):
            if self._add is not None:
                if callable(self._add): return self._add(a, b)
                if isinstance(self._add, list): return self._add[self.R.index(a)][self.R.index(b)]
                if isinstance(self._add, dict): return self._add.get((a, b), self._add.get(str((a, b))))
            return a + b

        def mul(self, a, b):
            if self._mul is not None:
                if callable(self._mul): return self._mul(a, b)
                if isinstance(self._mul, list): return self._mul[self.R.index(a)][self.R.index(b)]
                if isinstance(self._mul, dict): return self._mul.get((a, b), self._mul.get(str((a, b))))
            return a * b

    try:
        ring = RingWrapper(R, S, I, witness)
    except Exception:
        return [False, False, False, False]

    def contains(lst, item):
        for x in lst:
            if x == item: return True
        return False

    # Find zero
    zero = witness.get('zero')
    if zero is None:
        for z_cand in R:
            if all(ring.add(z_cand, a) == a for a in R):
                zero = z_cand
                break

    # Find one
    one = witness.get('one')
    if one is None:
        for o_cand in R:
            if all(ring.mul(o_cand, a) == a for a in R):
                one = o_cand
                break

    # Verify R is a valid ring
    try:
        is_ring = True
        if zero is None or one is None: is_ring = False
        if not contains(R, zero) or not contains(R, one): is_ring = False
        
        if is_ring:
            for a in R:
                if ring.add(a, zero) != a: is_ring = False
                if ring.add(zero, a) != a: is_ring = False
                if ring.mul(a, one) != a: is_ring = False
                if ring.mul(one, a) != a: is_ring = False
                
                has_inv = False
                for b in R:
                    if ring.add(a, b) == zero and ring.add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: is_ring = False

            for a in R:
                for b in R:
                    if not contains(R, ring.add(a, b)): is_ring = False
                    if not contains(R, ring.mul(a, b)): is_ring = False
                    if ring.add(a, b) != ring.add(b, a): is_ring = False
                    for c in R:
                        if ring.add(ring.add(a, b), c) != ring.add(a, ring.add(b, c)): is_ring = False
                        if ring.mul(ring.mul(a, b), c) != ring.mul(a, ring.mul(b, c)): is_ring = False
                        if ring.mul(a, ring.add(b, c)) != ring.add(ring.mul(a, b), ring.mul(a, c)): is_ring = False
                        if ring.mul(ring.add(a, b), c) != ring.add(ring.mul(a, c), ring.mul(b, c)): is_ring = False
        if not is_ring:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: S is a multiplicatively closed subset of R
    try:
        h1 = True
        if not contains(S, one): h1 = False
        for a in S:
            if not contains(R, a): h1 = False
            for b in S:
                if not contains(S, ring.mul(a, b)):
                    h1 = False
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        h2 = True
        if not contains(I, zero): h2 = False
        for a in I:
            if not contains(R, a): h2 = False
            for b in I:
                minus_b = None
                for x_elem in R:
                    if ring.add(b, x_elem) == zero:
                        minus_b = x_elem
                        break
                if minus_b is None or not contains(I, ring.add(a, minus_b)):
                    h2 = False
            for r in R:
                if not contains(I, ring.mul(a, r)): h2 = False
                if not contains(I, ring.mul(r, a)): h2 = False
    except Exception:
        h2 = False

    # H3: \bar{S} is the image of S in the quotient ring R/I
    # This is a definitional hypothesis setting up notation for the conclusion.
    h3 = True

    # neg_Q: The conclusion fails.
    # The conclusion states (S^{-1}R)/(S^{-1}I) is isomorphic to \bar{S}^{-1}(R/I).
    # For non-commutative rings, if S is a left Ore set, S^{-1}I might not be a right ideal.
    # If S^{-1}I is not a right ideal, it is not a two-sided ideal, so the quotient (S^{-1}R)/(S^{-1}I)
    # is not a ring, making the isomorphism statement false.
    try:
        neg_q = False
        
        # Check if S is a left Ore set (required for Ore localization S^{-1}R to exist)
        is_ore = True
        for r in R:
            for s in S:
                ore_found = False
                for v in S:
                    for u in R:
                        if ring.mul(v, r) == ring.mul(u, s):
                            ore_found = True
                            break
                    if ore_found: break
                if not ore_found:
                    is_ore = False
                    break
            if not is_ore: break
        
        if is_ore:
            # Helper to check if a fraction s^{-1}r is in S^{-1}I
            def in_S_inv_I(s_elem, r_elem):
                for u in R:
                    if contains(S, ring.mul(u, s_elem)) and contains(I, ring.mul(u, r_elem)):
                        return True
                return False

            # Check if S^{-1}I is a right ideal in S^{-1}R
            for s1 in S:
                for a in I:
                    for s2 in S:
                        for r in R:
                            # Compute product of x = s1^{-1}a in S^{-1}I and y = s2^{-1}r in S^{-1}R
                            # We need v in S, u in R such that v*a = u*s2
                            v_found, u_found = None, None
                            for v in S:
                                for u in R:
                                    if ring.mul(v, a) == ring.mul(u, s2):
                                        v_found, u_found = v, u
                                        break
                                if v_found is not None: break
                            
                            if v_found is not None:
                                prod_s = ring.mul(v_found, s1)
                                prod_r = ring.mul(u_found, r)
                                # If the product is not in S^{-1}I, it's not a right ideal
                                if not in_S_inv_I(prod_s, prod_r):
                                    neg_q = True
                                    break
                        if neg_q: break
                    if neg_q: break
                if neg_q: break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I is an ideal of R",
    "H_3: \\bar{S} is the image of S in the quotient ring R/I",
    "¬Q: S^{-1}I is not a right ideal in S^{-1}R, so the quotient (S^{-1}R)/(S^{-1}I) is not a ring"
]

N_HYP = 3
NEG_Q_INDEX = 3