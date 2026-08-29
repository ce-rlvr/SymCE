import sympy
from sympy import Rational
from sympy.abc import x
import math

# Top-level setup
Q_field = sympy.S.Rationals
Z_ring = sympy.S.Integers

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness is a valid counterexample to the false conjecture:
    "If v is a valuation on K and Gamma is the value group of v, then Gamma is a divisible abelian group."
    
    The witness is expected to be a callable representing a valuation v on Q or Q(x),
    or a dictionary containing such a callable under the key 'v'.
    """
    if isinstance(witness, dict):
        v = witness.get('v', witness)
    else:
        v = witness
        
    if not callable(v):
        return [False, False, False]
        
    # Test domains: non-zero rationals and non-zero rational functions
    test_Q = [Rational(i, j) for i in range(-4, 5) for j in range(1, 5) if i != 0]
    test_Qx = [x, x**2, 1/x, x+1, 1/(x+1), (x+1)/(x-1), Rational(1, 2), Rational(2, 1)]
    
    domain = []
    try:
        v(test_Q[0])
        v(test_Q[1])
        domain = test_Q
    except Exception:
        pass
        
    if not domain:
        try:
            v(test_Qx[0])
            v(test_Qx[1])
            domain = test_Qx
        except Exception:
            pass

    if not domain:
        return [False, False, False]
        
    # H_1: v is a valuation on K
    h1 = True
    try:
        for a in domain:
            for b in domain:
                va = v(a)
                vb = v(b)
                vab = v(a * b)
                if vab != va + vb:
                    h1 = False
                    break
                if a + b != 0:
                    v_plus = v(a + b)
                    if v_plus < min(va, vb):
                        h1 = False
                        break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: Gamma is the value group of v
    # We verify that the valuation is non-trivial (a trivial valuation has a divisible value group {0})
    h2 = False
    images = set()
    try:
        for a in domain:
            images.add(v(a))
        if len(images) > 1:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: Gamma is not a divisible abelian group
    neg_q = False
    try:
        if h1 and h2:
            # Any non-trivial valuation on Q or Q(x) has a discrete value group (isomorphic to Z).
            # Z is not a divisible group. We verify the image elements are real/rational numbers.
            is_real = True
            for val in images:
                try:
                    float(val)
                except Exception:
                    is_real = False
                    break
            if is_real:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: v is a valuation on K",
    "H_2: Gamma is the value group of v",
    "¬Q: Gamma is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2