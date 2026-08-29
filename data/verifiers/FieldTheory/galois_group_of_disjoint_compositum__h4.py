import sympy
from sympy import Symbol, minpoly, degree, factor_list, I, sqrt, Rational, QQ
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup for potential witness expressions
x = Symbol('x')

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple of two SymPy algebraic numbers (a, b),
    representing the extensions K = Q(a) and L = Q(b) over the base field F = Q.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    # We implicitly use F = Q (the field of rational numbers), which is a field.
    h1_ok = True
    
    # H_2: K and L are finite Galois extensions of F
    h2_ok = False
    try:
        p_a = minpoly(a, x)
        p_b = minpoly(b, x)
        
        deg_a = degree(p_a, x)
        deg_b = degree(p_b, x)
        
        # Check if K = Q(a) is Galois over Q by seeing if its minimal polynomial splits completely
        facs_a = factor_list(p_a, extension=[a])[1]
        a_galois = all(degree(f[0], x) == 1 for f in facs_a) and sum(f[1] for f in facs_a) == deg_a
        
        # Check if L = Q(b) is Galois over Q
        facs_b = factor_list(p_b, extension=[b])[1]
        b_galois = all(degree(f[0], x) == 1 for f in facs_b) and sum(f[1] for f in facs_b) == deg_b
        
        h2_ok = bool(a_galois and b_galois)
    except Exception:
        h2_ok = False
        
    # H_3: K and L are contained in a common extension field
    # Since a and b are algebraic numbers in C, they are both contained in C.
    h3_ok = False
    try:
        # Verify they can be combined algebraically
        _ = a + b
        h3_ok = True
    except Exception:
        h3_ok = False
        
    # ¬Q: Gal(KL/F) is not isomorphic to Gal(K/F) x Gal(L/F)
    neg_q_ok = False
    try:
        degs = []
        # Find the degree of the compositum KL = Q(a, b) over Q.
        # By the primitive element theorem, a + c*b is primitive for most c.
        for c in range(1, 10):
            try:
                p_c = minpoly(a + c*b, x)
                degs.append(degree(p_c, x))
            except Exception:
                pass
        if degs:
            deg_KL = max(degs)
            # If the degree of the compositum is not the product of the degrees,
            # the order of Gal(KL/F) differs from the order of Gal(K/F) x Gal(L/F),
            # hence they cannot be isomorphic.
            neg_q_ok = bool(deg_KL != deg_a * deg_b)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are finite Galois extensions of F",
    "H_3: K and L are contained in a common extension field",
    "¬Q: Gal(KL/F) is not isomorphic to Gal(K/F) x Gal(L/F)"
]

N_HYP = 3
NEG_Q_INDEX = 3