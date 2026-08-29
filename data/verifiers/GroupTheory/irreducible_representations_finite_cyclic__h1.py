import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, sympy.Matrix):
            witness = [witness]
    except Exception:
        pass

    # H_1: V is a finite-dimensional vector space over the complex numbers C
    h1_ok = False
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            if all(isinstance(M, sympy.Matrix) for M in witness):
                if all(M.rows == M.cols for M in witness):
                    n = witness[0].rows
                    if n >= 1 and all(M.rows == n for M in witness):
                        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: rho is an irreducible group representation of G
    h2_ok = False
    try:
        if h1_ok:
            n = witness[0].rows
            invertible = all(M.det() != 0 for M in witness)
            if invertible:
                if n == 1:
                    h2_ok = True
                else:
                    # By Burnside's Theorem, a representation over C is irreducible 
                    # iff the matrices span the full matrix algebra M_n(C).
                    basis_vectors = [list(sympy.eye(n))]
                    queue = [sympy.eye(n)]
                    is_irred = False
                    
                    while queue and not is_irred:
                        current = queue.pop(0)
                        for M in witness:
                            nxt = current * M
                            vec = list(nxt)
                            test_matrix = sympy.Matrix(basis_vectors + [vec])
                            if test_matrix.rank() > len(basis_vectors):
                                basis_vectors.append(vec)
                                queue.append(nxt)
                                if len(basis_vectors) == n**2:
                                    is_irred = True
                                    break
                    h2_ok = is_irred
    except Exception:
        h2_ok = False

    # neg_Q: The dimension of V is not exactly 1
    neg_q = False
    try:
        if h1_ok:
            n = witness[0].rows
            neg_q = (n != 1)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the complex numbers C",
    "H_2: rho is an irreducible group representation of G",
    "¬Q: The dimension of V is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2