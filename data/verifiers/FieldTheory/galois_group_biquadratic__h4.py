import sympy
from sympy import Rational, sqrt
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness references
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    We assume the field F is the field of rational numbers (QQ).
    The witness is expected to provide the elements a and b.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
            elif len(witness) >= 4:
                # Handles formats like (F, a, b, K)
                a, b = witness[1], witness[2]
            else:
                a, b = witness[0], witness[1]
        else:
            a, b = witness, witness
    except Exception:
        return [False] * 6

    # H_1: F is a field with characteristic not equal to 2
    # Assuming F = QQ, characteristic is 0 != 2.
    h1 = True

    # H_2: a and b are elements of F
    try:
        a = sympy.Rational(a)
        b = sympy.Rational(b)
        h2 = True
    except Exception:
        h2 = False

    # H_3: There is no element x in F such that x^2 = a
    try:
        if h2:
            h3 = not bool(sympy.sqrt(a).is_rational)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: There is no element z in F such that z^2 = ab
    try:
        if h2:
            h4 = not bool(sympy.sqrt(a * b).is_rational)
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F
    # This is true by definition of the witness context.
    h5 = True

    # ¬Q: The field extension K/F is not Galois with degree 4 and Galois group V4
    # The degree of the splitting field of (x^2 - a)(x^2 - b) over QQ is 4 
    # if and only if a, b, and ab are all non-squares in QQ.
    # If the degree is 4, the Galois group is V4.
    # Thus, the conclusion holds iff the degree is 4.
    # The negated conclusion holds iff the degree is NOT 4.
    try:
        if h2:
            is_a_sq = bool(sympy.sqrt(a).is_rational)
            is_b_sq = bool(sympy.sqrt(b).is_rational)
            is_ab_sq = bool(sympy.sqrt(a * b).is_rational)
            
            deg_is_4 = (not is_a_sq) and (not is_b_sq) and (not is_ab_sq)
            neg_q = not deg_is_4
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: There is no element x in F such that x^2 = a",
    "H_4: There is no element z in F such that z^2 = ab",
    "H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F",
    "¬Q: The field extension K/F is not Galois with degree 4 and Galois group V4"
]

N_HYP = 5
NEG_Q_INDEX = 5