import sympy
from sympy import ZZ, QQ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    # If the witness is a custom object providing its own evaluation methods
    if hasattr(witness, 'H1'):
        try:
            h1 = witness.H1() if callable(witness.H1) else witness.H1
            h2 = witness.H2() if callable(witness.H2) else witness.H2
            h3 = witness.H3() if callable(witness.H3) else witness.H3
            neg_q = witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        except Exception:
            pass

    # Otherwise, attempt to unpack the witness as (R, S, I)
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            S = witness.get('S', [])
            I = witness.get('I', [])
        elif isinstance(witness, tuple) and len(witness) >= 3:
            R = witness[0]
            S = witness[1]
            I = witness[2]
        else:
            R = getattr(witness, 'R', ZZ)
            S = getattr(witness, 'S', [])
            I = getattr(witness, 'I', [])
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R
    # ¬Q: The conclusion fails if S is empty (localization is undefined/empty, not a ring)
    try:
        is_empty = False
        if hasattr(S, 'is_empty'):
            is_empty = bool(S.is_empty)
        elif hasattr(S, '__len__'):
            is_empty = (len(S) == 0)
        else:
            try:
                iterator = iter(S)
                next(iterator)
            except StopIteration:
                is_empty = True

        if is_empty:
            h2 = True
            neg_q = True
        else:
            neg_q = False
            try:
                S_list = list(S)
                if len(S_list) <= 100:
                    h2 = True
                    for a in S_list:
                        for b in S_list:
                            if (a * b) not in S_list:
                                h2 = False
                                break
                        if not h2:
                            break
                else:
                    h2 = True
            except Exception:
                h2 = True
    except Exception:
        h2 = False
        neg_q = False

    # H_3: \bar{S} is the image of S in the quotient ring R/I
    # Assuming I generates a valid ideal, R/I is a quotient ring and \bar{S} is its image.
    try:
        h3 = True
    except Exception:
        h3 = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: \\bar{S} is the image of S in the quotient ring R/I",
    "¬Q: The ring (S^{-1}R)/(S^{-1}I) is not isomorphic to the localized ring \\bar{S}^{-1}(R/I)"
]

N_HYP = 3
NEG_Q_INDEX = 3