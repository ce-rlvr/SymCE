import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_cyclic_of_order(G, p):
    """Helper to check if G is isomorphic to the cyclic group Z/pZ."""
    try:
        if hasattr(G, 'is_isomorphic'):
            try:
                res = G.is_isomorphic(CyclicGroup(p))
                if res is not None:
                    return bool(res)
            except Exception:
                pass
        
        if hasattr(G, 'order') and G.order() == p:
            if sympy.isprime(p) or p == 1:
                return True
            if hasattr(G, 'elements'):
                for g in G.elements:
                    if g.order() == p:
                        return True
                return False
    except Exception:
        pass
    return False

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness can be a tuple (p, q) or (p, q, G).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                p, q, G = witness
            elif len(witness) == 2:
                p, q = witness
                G = CyclicGroup(p) if (isinstance(p, int) and p > 0) else None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: p, q are coprime integers with p > 0
    try:
        h1 = isinstance(p, int) and isinstance(q, int) and math.gcd(p, q) == 1 and p > 0
    except Exception:
        h1 = False

    # H_2: G is the fundamental group of L(p,q)
    # Mathematically, the fundamental group of L(p,q) is uniquely Z/pZ.
    try:
        if G is None:
            h2 = False
        else:
            h2 = is_cyclic_of_order(G, p)
    except Exception:
        h2 = False

    # ¬Q: G does NOT admit the presentation <x | x^p = 1> OR is NOT isomorphic to Z/pZ
    # Admitting that presentation is equivalent to being isomorphic to Z/pZ.
    try:
        if G is None:
            neg_q = True
        else:
            neg_q = not is_cyclic_of_order(G, p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p, q are coprime integers with p > 0",
    "H_2: G is the fundamental group of L(p,q)",
    "¬Q: G does not admit the presentation <x | x^p = 1> or is not isomorphic to Z/pZ"
]

N_HYP = 2
NEG_Q_INDEX = 2