import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    "H_1: P is the n x n permutation matrix associated with sigma",
    "H_2: The disjoint cycle decomposition of sigma consists of k cycles",
    "¬Q: The spectrum of P does not consist exactly of the l_j-th roots of unity, or the algebraic multiplicity of 1 is not exactly k"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    P = None
    sigma = None
    h1_ok = False
    h2_ok = False
    neg_q = False
    
    try:
        if isinstance(witness, list):
            if len(witness) > 0 and isinstance(witness[0], list):
                witness = Matrix(witness)
            elif len(witness) > 0 and isinstance(witness[0], int):
                witness = Permutation(witness)
                
        if isinstance(witness, tuple) and len(witness) == 2:
            P_cand, sigma_cand = witness
            if isinstance(P_cand, list):
                P_cand = Matrix(P_cand)
            if isinstance(sigma_cand, list):
                sigma_cand = Permutation(sigma_cand)
                
            if isinstance(P_cand, Matrix) and isinstance(sigma_cand, Permutation):
                n = sigma_cand.size
                if P_cand.rows == n and P_cand.cols == n:
                    is_row_perm = True
                    is_col_perm = True
                    for i in range(n):
                        for j in range(n):
                            if P_cand[i, j] == 1:
                                if sigma_cand(i) != j:
                                    is_row_perm = False
                                if sigma_cand(j) != i:
                                    is_col_perm = False
                            elif P_cand[i, j] == 0:
                                if sigma_cand(i) == j:
                                    is_row_perm = False
                                if sigma_cand(j) == i:
                                    is_col_perm = False
                            else:
                                is_row_perm = False
                                is_col_perm = False
                    if is_row_perm or is_col_perm:
                        P = P_cand
                        sigma = sigma_cand
                        h1_ok = True
                        
        elif isinstance(witness, Matrix):
            if witness.is_square:
                n = witness.rows
                is_perm = True
                perm_list = [0] * n
                for i in range(n):
                    row = list(witness[i, :])
                    if row.count(1) != 1 or row.count(0) != n - 1:
                        is_perm = False
                        break
                    perm_list[i] = row.index(1)
                if is_perm:
                    for j in range(n):
                        col = list(witness[:, j])
                        if col.count(1) != 1 or col.count(0) != n - 1:
                            is_perm = False
                            break
                if is_perm:
                    P = witness
                    sigma = Permutation(perm_list)
                    h1_ok = True
                    
        elif isinstance(witness, Permutation):
            sigma = witness
            n = sigma.size
            P = zeros(n, n)
            for i in range(n):
                P[i, sigma(i)] = 1
            h1_ok = True
    except Exception:
        pass

    try:
        if h1_ok and sigma is not None:
            # The standard disjoint cycle decomposition often omits fixed points (1-cycles).
            # Sympy's cyclic_form returns exactly the cycles of length >= 2.
            cycles = sigma.cyclic_form
            k = len(cycles)
            l = [len(c) for c in cycles]
            h2_ok = True
    except Exception:
        pass

    try:
        if h1_ok and h2_ok:
            n = P.rows
            I = eye(n)
            
            # The algebraic multiplicity of 1 is the dimension of the nullspace of P - I
            # (since permutation matrices are diagonalizable over C)
            alg_mult_1 = len((P - I).nullspace())
            
            x = sympy.Symbol('x')
            char_poly = P.charpoly(x).as_expr()
            
            expected_poly = sympy.Integer(1)
            for length in l:
                expected_poly *= (x**length - 1)
                
            poly_diff = sympy.simplify(char_poly - expected_poly)
            
            # The conclusion fails if the spectrum does not match exactly the roots of unity
            # for the k cycles, or if the algebraic multiplicity of 1 is not exactly k.
            if poly_diff != 0 or alg_mult_1 != k:
                neg_q = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q]