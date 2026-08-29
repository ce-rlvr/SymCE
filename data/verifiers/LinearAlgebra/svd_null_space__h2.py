import sympy
from sympy import MatrixBase, simplify, expand, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    A = None
    V = None
    
    if isinstance(witness, dict):
        A = witness.get('A')
        V = witness.get('V')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 4:
            A, U, Sigma, V = witness
        elif len(witness) >= 2:
            A, V = witness[0], witness[1]

    # H_1: A is an m x n matrix over C with rank r
    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    # neg_Q: The last n - r columns of V do NOT form an orthonormal basis for the null space of A
    try:
        if not isinstance(A, MatrixBase) or not isinstance(V, MatrixBase):
            q = False
        else:
            m, n = A.shape
            r = A.rank()
            nullity = n - r
            
            if nullity == 0:
                q = True
            else:
                if V.shape[1] < nullity or V.shape[0] != n:
                    q = False
                else:
                    last_cols = V[:, V.shape[1] - nullity:]
                    
                    is_orthonormal = True
                    for i in range(nullity):
                        for j in range(nullity):
                            dot_prod = (last_cols[:, i].H * last_cols[:, j])[0, 0]
                            dot_prod = simplify(expand(dot_prod))
                            if i == j:
                                if dot_prod != 1:
                                    is_orthonormal = False
                            else:
                                if dot_prod != 0:
                                    is_orthonormal = False
                    
                    in_null_space = True
                    for i in range(nullity):
                        prod = A * last_cols[:, i]
                        for val in prod:
                            if simplify(expand(val)) != 0:
                                in_null_space = False
                                break
                    
                    q = is_orthonormal and in_null_space
    except Exception:
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over C with rank r",
    "¬Q: The last n-r columns of V do not form an orthonormal basis for the null space of A"
]

N_HYP = 1
NEG_Q_INDEX = 1