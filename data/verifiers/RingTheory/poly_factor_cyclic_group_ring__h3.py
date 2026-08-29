import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    G = None
    n = None
    R = None
    
    try:
        if hasattr(witness, 'is_cyclic') or hasattr(witness, 'elements'):
            G = witness
            try:
                n = G.order()
            except Exception:
                pass
        elif isinstance(witness, tuple):
            for item in witness:
                if hasattr(item, 'is_cyclic') or hasattr(item, 'elements'):
                    G = item
                elif isinstance(item, (int, sympy.Integer)):
                    n = int(item)
                else:
                    R = item
    except Exception:
        pass

    h1 = True
    
    h2 = False
    try:
        if n is not None and n >= 1:
            h2 = True
    except Exception:
        pass

    neg_q = False
    try:
        if G is not None:
            if hasattr(G, 'is_cyclic'):
                neg_q = not G.is_cyclic
            elif hasattr(G, 'is_abelian'):
                if not G.is_abelian:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: n >= 1 is an integer",
    "not Q: The group ring is not isomorphic to the factor ring"
]

N_HYP = 2
NEG_Q_INDEX = 2