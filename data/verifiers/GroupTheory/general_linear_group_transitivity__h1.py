import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import eye, zeros
from sympy.ntheory import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def parse_witness(witness):
    if isinstance(witness, (int, sympy.Integer)):
        return 1, int(witness)
    if isinstance(witness, tuple) and len(witness) == 2:
        if isinstance(witness[0], (int, sympy.Integer)) and isinstance(witness[1], (int, sympy.Integer)):
            return int(witness[0]), int(witness[1])
    if hasattr(witness, 'order'):
        try:
            return 1, int(witness.order())
        except Exception:
            pass
    if isinstance(witness, str):
        w = witness.lower()
        if w in ['z', 'integer', 'integers']:
            return 1, 0
        if w in ['r', 'real', 'reals', 'q', 'rational', 'rationals', 'c', 'complex']:
            return 1, -1
    if hasattr(witness, '__len__'):
        try:
            l = len(witness)
            if l > 1:
                return 1, l
        except Exception:
            pass
    return None, None

def conditions(witness) -> list[bool]:
    n, m = parse_witness(witness)
    
    try:
        h1 = (n is not None and n >= 1)
    except Exception:
        h1 = False
        
    try:
        h2 = (n is not None and m is not None)
    except Exception:
        h2 = False
        
    try:
        if m is None:
            neg_q = False
        elif m == -1:
            neg_q = False
        elif m == 0:
            neg_q = True
        elif abs(m) == 1:
            neg_q = False
        else:
            neg_q = not isprime(abs(m))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The dimension of V is at least 1",
    "H_2: GL(V) is the general linear group of V",
    "¬Q: The natural action of GL(V) on V \\setminus {0} is NOT transitive"
]

N_HYP = 2
NEG_Q_INDEX = 2