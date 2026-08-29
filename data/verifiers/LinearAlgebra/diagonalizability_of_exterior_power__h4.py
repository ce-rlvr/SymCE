import itertools
import sympy
from sympy import Matrix, zeros, eye
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (T, k) or a dict with keys 'T' and 'k',
    where T is a matrix representing the linear operator and k is an integer.
    """
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            k = witness.get('k')
        elif isinstance(witness, tuple) and len(witness) == 2:
            T, k = witness
        else:
            return [False, False, False, False]
            
        if not hasattr(T, 'is_square'):
            T = Matrix(T)
    except Exception:
        return [False, False, False, False]
        
    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = hasattr(T, 'is_square') and T.is_square
    except Exception:
        h1 = False
        
    # H_2: T is a diagonalizable linear operator from V to V
    try:
        h2 = bool(T.is_diagonalizable())
    except Exception:
        h2 = False
        
    # H_3: k is an integer such that 1 <= k <= dim(V)
    try:
        h3 = int(k) == k and 1 <= k <= T.shape[0]
    except Exception:
        h3 = False
        
    # ¬Q: \Lambda^k T is not diagonalizable
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            n = T.shape[0]
            k_int = int(k)
            # The matrix of the k-th exterior power of T is given by its k x k minors
            indices = list(itertools.combinations(range(n), k_int))
            m = len(indices)
            Lambda_T = zeros(m, m)
            for i in range(m):
                for j in range(m):
                    sub_T = T[list(indices[i]), list(indices[j])]
                    Lambda_T[i, j] = sub_T.det()
            neg_q = not bool(Lambda_T.is_diagonalizable())
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a diagonalizable linear operator from V to V",
    "H_3: k is an integer such that 1 <= k <= dim(V)",
    "¬Q: \\Lambda^k T is not diagonalizable"
]

N_HYP = 3
NEG_Q_INDEX = 3