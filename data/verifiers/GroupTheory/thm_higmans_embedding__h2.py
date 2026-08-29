import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: G is a finitely generated group
    try:
        h1 = False
        if hasattr(witness, 'is_finitely_generated'):
            val = witness.is_finitely_generated
            if callable(val):
                val = val()
            h1 = bool(val)
        elif hasattr(witness, 'generators'):
            gens = list(witness.generators)
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: There does not exist a finitely presented group H such that G is isomorphic to a subgroup of H
    # By Higman's Embedding Theorem, a finitely generated group can be embedded in a finitely presented group
    # if and only if it is recursively presented.
    try:
        neg_q = False
        if hasattr(witness, 'can_embed_in_fp_group'):
            val = witness.can_embed_in_fp_group
            if callable(val):
                val = val()
            neg_q = not bool(val)
        elif hasattr(witness, 'is_recursively_presented'):
            val = witness.is_recursively_presented
            if callable(val):
                val = val()
            neg_q = not bool(val)
        elif hasattr(witness, 'is_finitely_presented'):
            val = witness.is_finitely_presented
            if callable(val):
                val = val()
            if val:
                neg_q = False
        elif hasattr(witness, 'relators'):
            rels = list(witness.relators)
            neg_q = False
        elif type(witness).__name__ in ['PermutationGroup', 'FpGroup', 'FreeGroup']:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: There does not exist a finitely presented group H such that G is isomorphic to a subgroup of H"
]

N_HYP = 1
NEG_Q_INDEX = 1