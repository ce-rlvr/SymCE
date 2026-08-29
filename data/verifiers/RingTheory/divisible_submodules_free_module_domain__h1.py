import sympy
from sympy.ntheory import isprime
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ZnRing:
    def __init__(self, n):
        self.n = n
    def __int__(self):
        return self.n
    def __str__(self):
        return f"Z_{self.n}"
    def __repr__(self):
        return f"ZnRing({self.n})"

Z4_ring = ZnRing(4)
Z6_ring = ZnRing(6)
Z8_ring = ZnRing(8)
Z9_ring = ZnRing(9)

CONDITION_LABELS = [
    "H_1: R is not a field",
    "H_2: M is a free module over R",
    "¬Q: M contains a non-zero divisible submodule"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract the ring R from the witness
        if isinstance(witness, dict):
            if 'R' in witness:
                R = witness['R']
            elif 'ring' in witness:
                R = witness['ring']
            elif 'n' in witness:
                R = witness['n']
            else:
                R = list(witness.values())[0]
        elif isinstance(witness, (tuple, list)):
            R = witness[0]
        else:
            R = witness
            
        # Handle standard infinite rings
        if R == sympy.ZZ:
            # Z is not a field, free modules over Z have no non-zero divisible submodules
            return [True, True, False]
        if R == sympy.QQ:
            # QQ is a field, free modules over QQ are divisible
            return [False, True, True]
            
        # Extract the modulus n for Z_n rings
        n = None
        if hasattr(R, 'n'):
            n = R.n
        elif hasattr(R, 'order'):
            n = R.order()
        else:
            n = int(R)
            
        if n is not None:
            n = abs(n)
            if n == 0:
                # Z_0 is isomorphic to Z
                return [True, True, False]
            if n == 1:
                # Z_1 is the zero ring
                return [True, True, False]
            if n > 1:
                # H_1: R is not a field (Z_n is a field iff n is prime)
                h1 = not isprime(n)
                
                # H_2: M is a free module over R
                # (We implicitly consider M = R^k, which is always a free module)
                h2 = True
                
                # ¬Q: M contains a non-zero divisible submodule
                # In any finite ring Z_n, every regular element is a unit.
                # Therefore, r * Z_n = Z_n for all regular elements r.
                # This means Z_n is a divisible module over itself.
                # Thus, any free module M = (Z_n)^k contains a non-zero divisible submodule.
                neg_q = True
                
                return [h1, h2, neg_q]
                
    except Exception:
        pass
        
    return [False, False, False]