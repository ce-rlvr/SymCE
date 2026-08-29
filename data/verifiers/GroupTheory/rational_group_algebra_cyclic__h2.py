import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic_group(G):
    if not getattr(G, 'is_group', False):
        return False
    try:
        n = G.order()
        if n == sympy.oo or n == float('inf'):
            return False
    except Exception:
        return False

    try:
        if hasattr(G, 'is_cyclic'):
            val = G.is_cyclic
            if callable(val):
                return bool(val())
            elif val is not None:
                return bool(val)
    except Exception:
        pass
            
    try:
        if hasattr(G, 'elements'):
            elems = G.elements
        else:
            elems = list(G.generate())
        for g in elems:
            if hasattr(g, 'order'):
                o = g.order() if callable(g.order) else g.order
                if o == n:
                    return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_cyclic_group(witness)
    except Exception:
        h1 = False

    try:
        if not getattr(witness, 'is_group', False):
            neg_q = False
        else:
            try:
                n = witness.order()
                if n == sympy.oo or n == float('inf'):
                    neg_q = False
                else:
                    neg_q = not is_cyclic_group(witness)
            except Exception:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n",
    "¬Q: The group algebra of G over Q is NOT isomorphic to the direct product of cyclotomic fields"
]

N_HYP = 1
NEG_Q_INDEX = 1