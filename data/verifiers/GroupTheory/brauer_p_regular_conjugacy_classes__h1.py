import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k is an algebraically closed field of characteristic p",
    "¬Q: The number of p-regular conjugacy classes in G is not equal to the number of isomorphism classes of simple kG-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    G = None
    p = None
    
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            p = witness[1]
        else:
            G = witness
            p = 2
    except Exception:
        pass

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: k is an algebraically closed field of characteristic p
    # This is a theoretical setup assumption. We assume it holds for the context.
    h2 = True

    # ¬Q: The conclusion fails (number of p-regular classes != number of simple modules)
    # Brauer's theorem holds for all finite groups. It fails for infinite groups.
    try:
        neg_q = False
        if hasattr(G, 'is_finite') and G.is_finite is False:
            neg_q = True
        elif hasattr(G, 'order'):
            if callable(G.order):
                if G.order() == sympy.oo:
                    neg_q = True
            else:
                if G.order == sympy.oo:
                    neg_q = True
        
        class_name = type(G).__name__
        if 'FreeGroup' in class_name:
            neg_q = True
        if G in (sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes):
            neg_q = True
        if isinstance(G, str) and G in ['Z', 'Q', 'R', 'C', 'FreeGroup']:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]