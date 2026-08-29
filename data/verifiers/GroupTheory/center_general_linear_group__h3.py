import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is an integer such that n >= 1",
    "¬Q: The center Z(GL_n(F)) is not the set of all matrices of the form cI for non-zero c in F"
]

def conditions(witness):
    """
    Given a witness (F, n), checks if it satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        F, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False) or getattr(F, 'is_field', False))
    except Exception:
        h1 = False
        
    # H_2: n is an integer such that n >= 1
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False
        
    # ¬Q: The center Z(GL_n(F)) is NOT the set of all matrices of the form cI for non-zero c in F.
    # For any ring F, the center of GL_n(F) consists of scalar matrices cI where c is a unit 
    # in the center of F (i.e., c in Z(F) intersect F^x).
    # The conclusion claims this set equals {cI | c in F \ {0}}.
    # This equality holds if and only if F \ {0} = Z(F) intersect F^x.
    # This requires every non-zero element to be a unit (F is a division ring) AND 
    # every non-zero element to be in the center (F is commutative).
    # Thus, the conclusion holds IF AND ONLY IF F is a commutative field.
    # Therefore, the conclusion FAILS (neg_Q is True) iff F is NOT a commutative field.
    try:
        is_f = bool(getattr(F, 'is_Field', False) or getattr(F, 'is_field', False))
        is_comm = bool(getattr(F, 'is_commutative', True))
        neg_q = not (is_f and is_comm)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]