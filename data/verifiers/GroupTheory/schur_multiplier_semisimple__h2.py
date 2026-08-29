import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for a semisimple finite group G, its Schur multiplier M(G)
    is isomorphic to the direct product of the Schur multipliers of its simple components.
    
    In the context of algebraic groups, a semisimple finite group is a central product 
    of quasisimple groups (which implies G is a perfect group). If G has a non-trivial center, 
    its Schur multiplier is strictly smaller than the direct product of the Schur multipliers 
    of its simple components, making it a counterexample.
    """
    try:
        # H_1: G is a semisimple finite group.
        # We verify this by checking if G is a non-trivial perfect group.
        h1 = False
        if hasattr(witness, 'is_abelian') and not witness.is_abelian:
            if witness.order() > 1 and witness.derived_subgroup().order() == witness.order():
                h1 = True
    except Exception:
        h1 = False

    try:
        # neg_Q: M(G) is NOT isomorphic to the direct product of M(S_i).
        # For a perfect group, this occurs exactly when G has a non-trivial center 
        # (i.e., G is a central product of quasisimple groups rather than a direct product).
        neg_q = False
        if h1:
            if witness.center().order() > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group (perfect group)",
    "¬Q: The Schur multiplier M(G) is NOT isomorphic to the direct product of M(S_i)"
]

N_HYP = 1
NEG_Q_INDEX = 1