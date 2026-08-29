import sympy
from sympy import Matrix, zeros, eye
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def kronecker_product(A, B):
    r1, c1 = A.shape
    r2, c2 = B.shape
    M = zeros(r1*r2, c1*c2)
    for i in range(r1):
        for j in range(c1):
            M[i*r2:(i+1)*r2, j*c2:(j+1)*c2] = A[i, j] * B
    return M

def dim_Hom(As, Bs):
    n = As[0].shape[0]
    m = Bs[0].shape[0]
    
    K_blocks = []
    for A, B in zip(As, Bs):
        K_i = kronecker_product(A.T, eye(m)) - kronecker_product(eye(n), B)
        K_blocks.append(K_i)
    
    total_rows = sum(K.shape[0] for K in K_blocks)
    K_stacked = zeros(total_rows, m * n)
    current_row = 0
    for K in K_blocks:
        r = K.shape[0]
        K_stacked[current_row:current_row+r, :] = K
        current_row += r
        
    return m * n - K_stacked.rank()

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        As, Bs = witness
        if not isinstance(As, (list, tuple)):
            As = [As]
        if not isinstance(Bs, (list, tuple)):
            Bs = [Bs]
        
        if all(isinstance(A, Matrix) and A.is_square for A in As) and \
           all(isinstance(B, Matrix) and B.is_square for B in Bs):
            if len(As) == len(Bs) and len(As) > 0:
                n = As[0].shape[0]
                m = Bs[0].shape[0]
                if all(A.shape[0] == n for A in As) and all(B.shape[0] == m for B in Bs):
                    return As, Bs
    return None, None

def conditions(witness):
    try:
        # Try matrix witness (representing modules over Q[x_1, ..., x_k])
        As, Bs = parse_witness(witness)
        if As is not None:
            h1 = True
            dim_AB = dim_Hom(As, Bs)
            h2 = (dim_AB == 0)
            dim_BA = dim_Hom(Bs, As)
            h3 = (dim_BA == 0)
            neg_q = (dim_AB + dim_BA > 0)
            return [h1, h2, h3, neg_q]
        
        # Try integer witness (representing Z_n and Z_m as Z-modules)
        if isinstance(witness, tuple) and len(witness) == 2:
            n, m = witness
            if isinstance(n, int) and isinstance(m, int):
                h1 = True
                g = math.gcd(abs(n), abs(m))
                h2 = (g == 1)
                h3 = (g == 1)
                neg_q = (g != 1)
                return [h1, h2, h3, neg_q]
            
            # Try group witness (representing Z_n and Z_m as Z-modules)
            if hasattr(n, 'order') and hasattr(m, 'order'):
                order_n = n.order()
                order_m = m.order()
                if getattr(n, 'is_abelian', False) and getattr(m, 'is_abelian', False):
                    h1 = True
                    g = math.gcd(order_n, order_m)
                    h2 = (g == 1)
                    h3 = (g == 1)
                    neg_q = (g != 1)
                    return [h1, h2, h3, neg_q]

        return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: M1 and M2 are R-modules",
    "H_2: Hom_R(M1, M2) = {0}",
    "H_3: Hom_R(M2, M1) = {0}",
    "¬Q: End_R(M1 \\oplus M2) is not isomorphic to End_R(M1) \\times End_R(M2)"
]

N_HYP = 3
NEG_Q_INDEX = 3