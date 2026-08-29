import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of phi is 2",
    "H_3: For all g in G, phi(g) = g implies g is the identity element",
    "not Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, phi = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'phi'):
            G = witness.G
            phi = witness.phi
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The order of phi is 2
    try:
        if not h1:
            h2 = False
        else:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            else:
                elements = list(G.generate())
                
            is_order_2 = True
            is_identity = True
            for g in elements:
                if isinstance(phi, dict):
                    phig = phi.get(g, None)
                    if phig is None:
                        is_order_2 = False
                        break
                    phiphig = phi.get(phig, None)
                else:
                    phig = phi(g)
                    phiphig = phi(phig)
                
                if phiphig != g:
                    is_order_2 = False
                    break
                if phig != g:
                    is_identity = False
            h2 = is_order_2 and not is_identity
    except Exception:
        h2 = False

    # H_3: For all g in G, phi(g) = g implies g is the identity element
    try:
        if not h1:
            h3 = False
        else:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            else:
                elements = list(G.generate())
                
            identity = None
            for e in elements:
                if e * e == e:
                    identity = e
                    break
            
            h3 = True
            for g in elements:
                if isinstance(phi, dict):
                    phig = phi.get(g, None)
                else:
                    phig = phi(g)
                
                if phig == g:
                    if g != identity:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # not Q: G is not a solvable group
    try:
        if not h1:
            neg_q = False
        else:
            if callable(G.is_solvable):
                neg_q = not G.is_solvable()
            else:
                neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]