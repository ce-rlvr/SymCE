import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup, free_group
)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness['F']
            H = witness['H']
        else:
            F, H = witness
    except Exception:
        return [False, False]

    # H_1: F is a free group of countable rank
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist an injective group homomorphism from F into H
    try:
        if type(F).__name__ != 'FreeGroup':
            neg_q = False
        else:
            r = len(F.generators)
            if r == 0:
                neg_q = False
            elif isinstance(H, PermutationGroup):
                # F is infinite (r >= 1), H is finite, so F cannot embed into H
                neg_q = True
            elif type(H).__name__ == 'FreeGroup':
                m = len(H.generators)
                if r == 1:
                    # F is isomorphic to Z. Embeds into H iff H is non-trivial
                    neg_q = not (m >= 1)
                else:
                    # F is non-abelian free. Embeds into H iff H contains a non-abelian free group
                    neg_q = not (m >= 2)
            else:
                # For unsupported group types, we cannot definitively verify the lack of embedding
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of countable rank",
    "¬Q: There does not exist an injective group homomorphism from F into H"
]

N_HYP = 1
NEG_Q_INDEX = 1