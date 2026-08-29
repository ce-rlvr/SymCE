import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: The multiplicative group of units modulo p^k is not cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
        else:
            p, k = witness
    except Exception:
        return [False, False]
        
    # H1: k is a positive integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and k > 0
    except Exception:
        h1 = False
        
    # neg_Q: The multiplicative group of units modulo p^k is NOT cyclic
    try:
        if not h1 or not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            n = abs(int(p)**int(k))
            if n == 0:
                neg_q = False
            elif n in (1, 2, 4):
                neg_q = False
            else:
                factors = factorint(n)
                if len(factors) == 1:
                    prime = list(factors.keys())[0]
                    is_cyclic = (prime != 2)
                elif len(factors) == 2:
                    is_cyclic = (2 in factors and factors[2] == 1)
                else:
                    is_cyclic = False
                neg_q = not is_cyclic
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]