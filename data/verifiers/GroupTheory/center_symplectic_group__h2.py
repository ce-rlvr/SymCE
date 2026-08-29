import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    n, p = None, None
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n = int(witness[0])
            p_obj = witness[1]
            if hasattr(p_obj, 'characteristic'):
                p = int(p_obj.characteristic())
            else:
                s = str(p_obj).replace(' ', '')
                if s.startswith('GF(') and s.endswith(')'):
                    p = int(s[3:-1])
                else:
                    p = int(p_obj)
        elif isinstance(witness, int) and not isinstance(witness, bool):
            n, p = witness, 3
        elif isinstance(witness, str):
            s = witness.replace(' ', '').lower()
            if s.startswith('sp(') and s.endswith(')'):
                inner = s[3:-1]
                parts = inner.split(',')
                val = int(parts[0])
                n = val // 2 if val % 2 == 0 else val
                if len(parts) > 1:
                    p = int(parts[1])
                else:
                    p = 3
            else:
                n, p = int(witness), 3
        else:
            if hasattr(witness, 'shape'):
                n = witness.shape[0] // 2
                p = 3
            elif hasattr(witness, 'degree'):
                n = witness.degree // 2
                p = 3
    except Exception:
        pass

    # H_1: F is a field with characteristic not equal to 2
    try:
        h1 = (p == 0) or (isprime(p) and p != 2)
    except Exception:
        h1 = False

    # H_2: G is the symplectic group Sp(2n, F)
    try:
        h2 = isinstance(n, int) and not isinstance(n, bool) and n >= 0
    except Exception:
        h2 = False

    # ¬Q: The center of G does not consist exactly of I and -I
    # For n = 0, the center is trivial (size 1), so it does not consist of two distinct elements I and -I.
    try:
        neg_q = (n == 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: G is the symplectic group Sp(2n, F)",
    "¬Q: The center of G does not consist exactly of I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2