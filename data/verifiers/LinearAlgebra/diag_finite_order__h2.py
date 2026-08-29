import sympy
from sympy import Matrix, eye, zeros, Symbol, Poly
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    try:
        F, A, k = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H2: There exists an integer k >= 1 such that A^k = I
    try:
        if int(k) != k or k < 1:
            h2 = False
        else:
            n = A.shape[0]
            A_k = A**k
            h2 = True
            for i in range(n):
                for j in range(n):
                    expected_int = 1 if i == j else 0
                    if A_k[i, j] == expected_int:
                        continue
                    try:
                        val = F.from_sympy(A_k[i, j])
                        expected_F = F.one if i == j else F.zero
                        if val != expected_F:
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # H3: The characteristic of F does not divide k
    try:
        char = F.characteristic()
        if char == 0:
            h3 = True
        else:
            h3 = bool(k % char != 0)
    except Exception:
        h3 = False
        
    # H4: The polynomial x^k - 1 splits into linear factors over F
    try:
        x = Symbol('x')
        poly = Poly(x**k - 1, x, domain=F)
        factors = poly.factor_list()
        h4 = all(f.degree() == 1 for f, m in factors[1])
    except Exception:
        h4 = False
        
    # ¬Q: A is not diagonalizable over F
    try:
        n = A.shape[0]
        try:
            A_F = [[F.from_sympy(A[i, j]) for j in range(n)] for i in range(n)]
            is_matrix_over_F = True
        except Exception:
            is_matrix_over_F = False
            
        if not is_matrix_over_F:
            neg_q = True
        else:
            cp = A.charpoly(x)
            cp_F = Poly(cp.as_expr(), x, domain=F)
            factors = cp_F.factor_list()
            
            is_diag = True
            for factor, mult in factors[1]:
                if factor.degree() != 1:
                    is_diag = False
                    break
                    
            if is_diag:
                for factor, mult in factors[1]:
                    c = factor.coeffs()[0]
                    d = factor.coeffs()[1] if len(factor.coeffs()) > 1 else F.zero
                    root = F.exquo(F.neg(d), c)
                    
                    M = [[A_F[i][j] for j in range(n)] for i in range(n)]
                    for i in range(n):
                        M[i][i] = F.sub(M[i][i], root)
                        
                    rank = 0
                    r = 0
                    cols = 0
                    while r < n and cols < n:
                        pivot_r = r
                        while pivot_r < n and M[pivot_r][cols] == F.zero:
                            pivot_r += 1
                        if pivot_r == n:
                            cols += 1
                            continue
                        M[r], M[pivot_r] = M[pivot_r], M[r]
                        inv_pivot = F.exquo(F.one, M[r][cols])
                        for j in range(cols, n):
                            M[r][j] = F.mul(M[r][j], inv_pivot)
                        for i in range(n):
                            if i != r:
                                factor_val = M[i][cols]
                                for j in range(cols, n):
                                    M[i][j] = F.sub(M[i][j], F.mul(factor_val, M[r][j]))
                        rank += 1
                        r += 1
                        cols += 1
                        
                    nullity = n - rank
                    if nullity != mult:
                        is_diag = False
                        break
            neg_q = not is_diag
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: There exists an integer k >= 1 such that A^k = I",
    "H_3: The characteristic of F does not divide k",
    "H_4: The polynomial x^k - 1 splits into linear factors over F",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 4
NEG_Q_INDEX = 4