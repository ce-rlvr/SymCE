import sympy
from sympy import QQ, ZZ
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    H1: k is a field
    H2: R is finitely generated as a k-algebra
    H3: I is an ideal of R
    neg_Q: The quotient ring R/I is NOT finitely generated as a k-algebra
    """
    try:
        if isinstance(witness, dict):
            k = witness.get('k')
            R = witness.get('R')
            I = witness.get('I')
        elif isinstance(witness, tuple) and len(witness) == 3:
            k, R, I = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: k is a field
    try:
        h1 = bool(getattr(k, 'is_Field', False))
    except Exception:
        h1 = False

    # H2: R is finitely generated as a k-algebra
    try:
        if hasattr(R, 'is_finitely_generated_algebra'):
            h2 = bool(R.is_finitely_generated_algebra(k))
        elif hasattr(R, 'domain') and R.domain == k and hasattr(R, 'gens'):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: I is an ideal of R
    try:
        if hasattr(I, 'is_ideal'):
            h3 = bool(I.is_ideal(R))
        elif isinstance(I, (list, tuple, set)):
            h3 = all(e in R for e in I)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: R/I is NOT finitely generated as a k-algebra
    try:
        if hasattr(witness, 'is_quotient_fg'):
            neg_q = not bool(witness.is_quotient_fg())
        else:
            # Mathematically, the quotient of a finitely generated algebra by an ideal
            # is always finitely generated, as the generators of R map to generators of R/I.
            # Thus, if H2 and H3 hold, the conclusion is true, so neg_Q is False.
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: R is finitely generated as a k-algebra",
    "H_3: I is an ideal of R",
    "¬Q: The quotient ring R/I is not finitely generated as a k-algebra"
]

N_HYP = 3
NEG_Q_INDEX = 3