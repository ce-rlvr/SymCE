import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import Permutation
from sympy import lcm, eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_exponent(G):
    """Computes the exponent of a finite group."""
    if hasattr(G, 'elements'):
        # Prevent timeouts on excessively large groups
        try:
            order = G.order() if callable(G.order) else G.order
            if order > 5000:
                raise ValueError("Group too large to compute exponent safely")
        except Exception:
            pass
        
        e = 1
        for g in G.elements:
            e = sympy.lcm(e, g.order())
        return int(e)
    raise ValueError("Cannot compute exponent: not a valid finite group")

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a group with finite exponent
    try:
        exp_G = get_exponent(G)
        h1 = (exp_G > 0)
    except Exception:
        h1 = False

    # ¬Q: The exponent of G x H is not equal to lcm(exp(G), exp(H))
    try:
        from sympy.combinatorics import DirectProduct
        exp_G = get_exponent(G)
        exp_H = get_exponent(H)
        GxH = DirectProduct(G, H)
        exp_GxH = get_exponent(GxH)
        
        q = (exp_GxH == sympy.lcm(exp_G, exp_H))
        neg_q = not q
    except Exception:
        # If Q cannot be evaluated (e.g., H is not a group or lacks a finite exponent),
        # the conclusion fails to hold, making ¬Q True.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group with finite exponent",
    "¬Q: The exponent of G x H is not equal to lcm(exp(G), exp(H))"
]

N_HYP = 1
NEG_Q_INDEX = 1