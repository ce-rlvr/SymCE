import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        x, y, z, n = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: x, y in F such that commutator != 1
    try:
        h1 = bool(x * y != y * x)
    except Exception:
        h1 = False
        
    # H2: z in F
    try:
        _ = x * z
        _ = z * x
        h2 = True
    except Exception:
        h2 = False
        
    # H3: n is an integer such that z**n == commutator
    try:
        is_int = False
        if isinstance(n, int):
            is_int = True
        elif hasattr(n, 'is_integer'):
            if callable(n.is_integer):
                is_int = n.is_integer()
            else:
                is_int = bool(n.is_integer)
                
        if not is_int:
            h3 = False
        else:
            n_int = int(n)
            try:
                inv_x = x**-1
            except Exception:
                inv_x = ~x
            try:
                inv_y = y**-1
            except Exception:
                inv_y = ~y
                
            comm1 = inv_x * inv_y * x * y
            comm2 = x * y * inv_x * inv_y
            
            try:
                zn = z**n_int
            except Exception:
                if n_int < 0:
                    try:
                        inv_z = z**-1
                    except Exception:
                        inv_z = ~z
                    zn = inv_z**(-n_int)
                else:
                    zn = None
            
            h3 = bool((zn == comm1) or (zn == comm2))
    except Exception:
        h3 = False
        
    # neg_Q: n != 1 and n != -1
    try:
        neg_q = bool(n != 1 and n != -1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x, y in F such that commutator(x, y) != 1",
    "H_2: z in F",
    "H_3: n is an integer such that z^n = commutator(x, y)",
    "¬Q: n != 1 and n != -1"
]

N_HYP = 3
NEG_Q_INDEX = 3