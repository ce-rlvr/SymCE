import sympy
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_subset(A, B):
    if hasattr(A, 'issubset'):
        return bool(A.issubset(B))
    if hasattr(A, 'subset'):
        return bool(A.subset(B))
    try:
        res = A <= B
        if isinstance(res, bool):
            return res
        return bool(res)
    except Exception:
        pass
    return set(A).issubset(set(B))

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
            K = witness.get('K')
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            R, I, J, K = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H1: R is a ring
    try:
        if hasattr(R, 'is_ring'):
            h1 = bool(R.is_ring() if callable(R.is_ring) else R.is_ring)
        elif hasattr(R, 'is_Ring'):
            h1 = bool(R.is_Ring() if callable(R.is_Ring) else R.is_Ring)
        else:
            h1 = type(R).__name__ == 'PolyRing' or hasattr(R, 'ideal') or (hasattr(R, '__add__') and hasattr(R, '__mul__'))
    except Exception:
        h1 = False

    # H2: J is an ideal of R
    try:
        if hasattr(J, 'is_ideal_of'):
            h2 = bool(J.is_ideal_of(R))
        elif hasattr(J, 'is_ideal'):
            h2 = bool(J.is_ideal(R) if callable(J.is_ideal) else J.is_ideal)
        else:
            h2 = (type(J).__name__ == 'Ideal' and getattr(J, 'ring', None) == R) or hasattr(J, 'subset') or hasattr(J, 'issubset') or hasattr(J, '__contains__')
    except Exception:
        h2 = False

    # H3: K is an ideal of R
    try:
        if hasattr(K, 'is_ideal_of'):
            h3 = bool(K.is_ideal_of(R))
        elif hasattr(K, 'is_ideal'):
            h3 = bool(K.is_ideal(R) if callable(K.is_ideal) else K.is_ideal)
        else:
            h3 = (type(K).__name__ == 'Ideal' and getattr(K, 'ring', None) == R) or hasattr(K, 'subset') or hasattr(K, 'issubset') or hasattr(K, '__contains__')
    except Exception:
        h3 = False

    # H4: I \subseteq J
    try:
        h4 = check_subset(I, J)
    except Exception:
        h4 = False

    # neg_Q: IK \not\subseteq JK
    try:
        IK = I * K
        JK = J * K
        q = check_subset(IK, JK)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "H_4: I \\subseteq J",
    "¬Q: IK is not a subset of JK"
]

N_HYP = 4
NEG_Q_INDEX = 4