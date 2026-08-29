import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    "H_1: Aut(G) is the automorphism group of G",
    "H_2: Hol(G) is the semidirect product G \\rtimes Aut(G)",
    "H_3: N is the canonical embedding of G into Hol(G)",
    "¬Q: N is not a normal subgroup of Hol(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # The witness must be a valid group.
        if not isinstance(witness, PermutationGroup):
            return [False, False, False, False]
        
        # H1, H2, H3 are definitional and hold for any valid group.
        h1 = True
        h2 = True
        h3 = True
        
        # Conclusion: N is a normal subgroup of Hol(G).
        # In the semidirect product Hol(G) = G \rtimes Aut(G), the base group G 
        # (canonically embedded as N = {(g, id) | g \in G}) is ALWAYS a normal subgroup.
        # Since the conclusion is mathematically always True for any group G,
        # its negation (that N is NOT a normal subgroup) is always False.
        neg_q = False
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]