import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
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
    "H_1: R is a commutative Artinian ring",
    "¬Q: P is not the annihilator of any non-zero element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness is expected to be a tuple (R_def, P_def)
        # R_def can be an integer n >= 2 (representing Z_n) 
        # or a list of integers (representing a product of Z_{n_i})
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        
        R_def, P_def = witness
        
        if isinstance(R_def, int):
            n = R_def
            if n < 2:
                return [False, False]
            elements = list(range(n))
            zero = 0
            def mul(a, b): return (a * b) % n
            
            if isinstance(P_def, int):
                P_set = set((P_def * i) % n for i in range(n))
            elif callable(P_def):
                P_set = set(y for y in elements if P_def(y))
            else:
                P_set = set(int(p) % n for p in P_def)
                
        elif isinstance(R_def, (list, tuple)) and all(isinstance(x, int) for x in R_def):
            if any(ni < 2 for ni in R_def):
                return [False, False]
            elements = list(itertools.product(*(range(ni) for ni in R_def)))
            zero = tuple(0 for _ in R_def)
            def mul(a, b): return tuple((x * y) % ni for x, y, ni in zip(a, b, R_def))
            
            if callable(P_def):
                P_set = set(y for y in elements if P_def(y))
            else:
                P_set = set(tuple(p) for p in P_def)
        else:
            return [False, False]
            
        # H1: R is a commutative Artinian ring
        # Finite commutative rings (like Z_n and their products) are always Artinian.
        h1 = True
        
        # Check if P is the annihilator of some non-zero element x in R
        is_associated = False
        for x in elements:
            if x == zero:
                continue
            ann_x = set(y for y in elements if mul(x, y) == zero)
            if ann_x == P_set:
                is_associated = True
                break
                
        # ¬Q: P is NOT the annihilator of any non-zero element
        neg_q = not is_associated
        
        return [h1, neg_q]
    except Exception:
        return [False, False]