import sympy
from sympy import symbols, Rational, Integer
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    "H_1: R is a commutative Noetherian ring",
    "¬Q: I is primary is not equivalent to having exactly one associated prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 3:
            h1 = bool(witness[0])
            is_prim = bool(witness[1])
            ass_primes = witness[2]
            num_ass_primes = ass_primes if isinstance(ass_primes, int) else len(ass_primes)
            q = (is_prim == (num_ass_primes == 1))
            neg_q = not q
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, int):
            h1 = True
            n = abs(witness)
            if n == 0:
                is_prim = True
            elif n == 1:
                is_prim = False
            else:
                factors = sympy.factorint(n)
                is_prim = (len(factors) == 1)
            
            num_ass_primes = 1
            q = (is_prim == (num_ass_primes == 1))
            neg_q = not q
            return [h1, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_noetherian', True))
        else:
            val = getattr(witness, 'is_commutative_noetherian', True)
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            is_prim = bool(witness['is_primary'])
            ass_primes = witness['associated_primes']
        else:
            val_prim = getattr(witness, 'is_primary')
            is_prim = bool(val_prim() if callable(val_prim) else val_prim)
            
            val_ass = getattr(witness, 'associated_primes')
            ass_primes = val_ass() if callable(val_ass) else val_ass
            
        num_ass_primes = ass_primes if isinstance(ass_primes, int) else len(ass_primes)
        q = (is_prim == (num_ass_primes == 1))
        neg_q = not q
    except Exception:
        pass

    return [h1, neg_q]