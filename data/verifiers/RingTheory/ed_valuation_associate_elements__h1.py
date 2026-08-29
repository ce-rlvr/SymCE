import sympy
from sympy import rem
import sympy.combinatorics.named_groups
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 3:
            a, b, d = witness
        elif len(witness) == 4:
            _, a, b, d = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: a and b are non-zero elements of R
    try:
        h1 = (a != 0) and (b != 0)
    except Exception:
        h1 = False

    # H2: a is an associate of b
    try:
        h2 = False
        if hasattr(a, 'is_associate'):
            h2 = a.is_associate(b)
        else:
            try:
                if a % b == 0 and b % a == 0:
                    h2 = True
            except Exception:
                if rem(a, b) == 0 and rem(b, a) == 0:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: d(a) != d(b)
    try:
        if isinstance(d, dict):
            da = d[a]
            db = d[b]
        else:
            da = d(a)
            db = d(b)
        neg_q = (da != db)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "H_2: a is an associate of b",
    "¬Q: d(a) != d(b)"
]

N_HYP = 2
NEG_Q_INDEX = 2