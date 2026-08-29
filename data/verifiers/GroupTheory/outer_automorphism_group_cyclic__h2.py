import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
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
    try:
        if hasattr(G, 'is_cyclic'):
            res = G.is_cyclic
            if callable(res):
                res = res()
            if res is not None:
                return bool(res)
        
        order = G.order
        if callable(order):
            order = order()
            
        elements = G.elements
        if callable(elements):
            elements = elements()
            
        for g in elements:
            o = g.order
            if callable(o):
                o = o()
            if o == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_cyclic_group(witness)
    except Exception:
        h1 = False

    # H2 is a definitional hypothesis
    h2 = True

    try:
        # For finite groups, Out(G) is isomorphic to Aut(G) iff Inn(G) is trivial.
        # Inn(G) is trivial iff G is abelian.
        # Thus, Out(G) is NOT isomorphic to Aut(G) iff G is NOT abelian.
        is_ab = witness.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
        neg_q = not bool(is_ab)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: Out(G) is defined as Aut(G)/Inn(G)",
    "¬Q: Out(G) is not isomorphic to Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2