import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_number(x):
    return isinstance(x, (int, float, complex)) or hasattr(x, 'is_Rational') or hasattr(x, 'is_Number') or isinstance(x, sympy.Expr)

def is_vector(v):
    if not isinstance(v, (list, tuple)): return False
    return all(is_number(x) for x in v)

def get_vectors(W):
    if isinstance(W, Matrix):
        return [tuple(W.row(i)) for i in range(W.rows)]
    elif isinstance(W, (list, tuple, set)):
        return [tuple(v) for v in W]
    return None

def conditions(witness):
    try:
        W1_raw, W2_raw = witness
        W1 = get_vectors(W1_raw)
        W2 = get_vectors(W2_raw)
        
        if W1 is None or W2 is None:
            return [False, False, False, False]
            
        h1 = False
        if all(is_vector(v) for v in W1) and all(is_vector(v) for v in W2):
            lens = set(len(v) for v in W1) | set(len(v) for v in W2)
            if len(lens) <= 1:
                h1 = True
                
        h2 = h1
        h3 = h1
        
        neg_q = False
        if h1:
            n = list(lens)[0] if lens else 0
            set_W1 = set(W1)
            set_W2 = set(W2)
            intersection_set = set_W1.intersection(set_W2)
            
            if not W1 or not W2:
                dim_intersection = 0
            else:
                M1 = Matrix(W1).T
                M2 = Matrix(W2).T
                M_block = M1.row_join(-M2)
                nullspace = M_block.nullspace()
                
                intersection_basis = []
                for vec in nullspace:
                    x = vec[:M1.cols, :]
                    intersection_basis.append(M1 * x)
                
                if intersection_basis:
                    M_int = intersection_basis[0]
                    for v in intersection_basis[1:]:
                        M_int = M_int.row_join(v)
                    dim_intersection = M_int.rank()
                else:
                    dim_intersection = 0
                    
            zero_vec = tuple([0]*n)
            
            if dim_intersection > 0:
                subspace_equals_set = False
            else:
                subspace_equals_set = (intersection_set == {zero_vec})
                
            neg_q = not subspace_equals_set
            
    except Exception:
        h1 = h2 = h3 = neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: W_1^0 and W_2^0 are the annihilators of W_1 and W_2 in V^*",
    "H_3: ^0U denotes the pre-annihilator in V of a subspace U",
    "¬Q: ^0(W_1^0 + W_2^0) != W_1 \\cap W_2"
]

N_HYP = 3
NEG_Q_INDEX = 3