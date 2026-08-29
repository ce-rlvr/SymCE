import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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

CONDITION_LABELS = [
    "H_1: Let V \\oplus W denote the external direct sum of V and W",
    "¬Q: dim(V \\oplus W) != dim(V) + dim(W)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        H1 = True
        neg_Q = False
        
        if isinstance(witness, tuple):
            # Interpretation 1: Vector spaces over different fields
            # witness = (dim_V, deg_F, dim_W, deg_K)
            # where deg_F and deg_K are the degrees of the fields over their intersection
            if len(witness) == 4:
                dim_V, deg_F, dim_W, deg_K = witness
                dim_V_oplus_W = dim_V * deg_F + dim_W * deg_K
                conjecture_holds = (dim_V_oplus_W == dim_V + dim_W)
                neg_Q = not conjecture_holds
                return [H1, neg_Q]
                
            # Interpretation 2: Modules over a ring (e.g., Z/nZ and Z/mZ)
            # witness = (n, m) or (Z_n, Z_m)
            # "dim" corresponds to the minimal number of generators
            elif len(witness) == 2:
                n, m = witness
                
                # Extract order if they are SymPy Group objects
                if hasattr(n, 'order') and callable(n.order):
                    n = n.order()
                elif hasattr(n, 'order'):
                    n = n.order
                    
                if hasattr(m, 'order') and callable(m.order):
                    m = m.order()
                elif hasattr(m, 'order'):
                    m = m.order
                    
                if isinstance(n, int) and isinstance(m, int) and n > 0 and m > 0:
                    def min_gens(k): 
                        return 1 if k > 1 else 0
                        
                    dim_V = min_gens(n)
                    dim_W = min_gens(m)
                    
                    if n == 1 and m == 1:
                        dim_V_oplus_W = 0
                    elif n == 1:
                        dim_V_oplus_W = min_gens(m)
                    elif m == 1:
                        dim_V_oplus_W = min_gens(n)
                    else:
                        # By Chinese Remainder Theorem, Z/nZ \oplus Z/mZ is cyclic iff gcd(n, m) == 1
                        dim_V_oplus_W = 1 if math.gcd(n, m) == 1 else 2
                        
                    conjecture_holds = (dim_V_oplus_W == dim_V + dim_W)
                    neg_Q = not conjecture_holds
                    return [H1, neg_Q]
                    
        return [False, False]
    except Exception:
        return [False, False]