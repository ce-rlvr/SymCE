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
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: G is non-abelian
    try:
        if hasattr(witness, 'is_abelian'):
            h1 = bool(not witness.is_abelian)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: Aut(G) is trivial (i.e., does NOT contain a non-trivial element)
    try:
        if not hasattr(witness, 'is_abelian') or not hasattr(witness, 'order'):
            neg_q = False
        elif not witness.is_abelian:
            # If G is non-abelian, its inner automorphism group Inn(G) is non-trivial.
            # Since Inn(G) <= Aut(G), Aut(G) is also non-trivial.
            neg_q = False
        else:
            # For abelian groups, the inversion map x -> x^-1 is an automorphism.
            # It is trivial iff x^2 = 1 for all x (i.e., G is an elementary abelian 2-group).
            # The automorphism group of (Z_2)^k is GL(k, 2), which is trivial iff k <= 1.
            # Therefore, for finite groups, Aut(G) is trivial iff |G| <= 2.
            neg_q = bool(witness.order() <= 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is non-abelian",
    "¬Q: Aut(G) is trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1