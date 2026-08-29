import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Symbol, roots, factor_list

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (F, a, b), checks the hypotheses and the negated conclusion.
    F should be a SymPy field (e.g., sympy.QQ, sympy.GF(p)).
    """
    try:
        F, a, b = witness
    except Exception:
        return [False, False, False, False, False]

    x = Symbol('x')

    # H_1: F is a field of characteristic not equal to 2
    try:
        h1 = F.is_Field and F.characteristic != 2
    except Exception:
        h1 = False

    # H_2: a is not a square in F
    try:
        rts_a = roots(x**2 - a, domain=F)
        h2 = len(rts_a) == 0
    except Exception:
        h2 = False

    # H_3: b is not a square in F
    try:
        rts_b = roots(x**2 - b, domain=F)
        h3 = len(rts_b) == 0
    except Exception:
        h3 = False

    # H_4: ab is not a square in F
    try:
        rts_ab = roots(x**2 - a*b, domain=F)
        h4 = len(rts_ab) == 0
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is NOT x^4 - 2(a+b)x^2 + (a-b)^2
    # This is true if the polynomial P(x) = x^4 - 2(a+b)x^2 + (a-b)^2 is reducible over F,
    # meaning it is not the minimal polynomial (which must be irreducible).
    try:
        P = x**4 - 2*(a+b)*x**2 + (a-b)**2
        facs = factor_list(P, domain=F)
        # facs[1] contains the factors and their multiplicities.
        # P is irreducible if there is exactly 1 factor and its multiplicity is 1.
        is_irreducible = (len(facs[1]) == 1 and facs[1][0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: a is not a square in F",
    "H_3: b is not a square in F",
    "H_4: ab is not a square in F",
    "¬Q: The minimal polynomial of sqrt(a) + sqrt(b) over F is not x^4 - 2(a+b)x^2 + (a-b)^2"
]

N_HYP = 4
NEG_Q_INDEX = 4