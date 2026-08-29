import sympy
from sympy import Matrix, eye, zeros, Symbol
import math
import itertools

# Setup
x = Symbol('x')
a, b, c, d, e, f, g, h = sympy.symbols('a b c d e f g h', commutative=False)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def leibniz_det(mat):
    """
    Computes the determinant using the Leibniz formula (row expansion).
    This is safe for matrices with non-commutative entries, unlike standard
    determinant algorithms (like Bareiss) which assume commutativity.
    """
    n = mat.shape[0]
    det_val = 0
    for p in itertools.permutations(range(n)):
        inv_count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if p[i] > p[j]:
                    inv_count += 1
        sign = 1 if inv_count % 2 == 0 else -1
        
        term = sign
        for i in range(n):
            term = term * mat[i, p[i]]
        det_val += term
    return det_val

def conditions(witness):
    try:
        H1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        H1 = False

    try:
        # H2 is definitional; if A is a square matrix, its characteristic polynomial
        # is defined as det(xI - A). We compute it to check the conclusion.
        H2 = H1
    except Exception:
        H2 = False

    try:
        if not H1:
            neg_Q = False
        else:
            n = witness.shape[0]
            M = x * eye(n) - witness
            
            # Use Leibniz determinant for small matrices to safely handle non-commutative entries
            if n <= 5:
                p = leibniz_det(M)
            else:
                p = M.det()
            
            deg = n
            coeffs = []
            # Extract coefficients of the characteristic polynomial p_A(x)
            for i in range(deg, -1, -1):
                c_i = p
                for _ in range(i):
                    c_i = sympy.diff(c_i, x)
                c_i = c_i.subs(x, 0) / math.factorial(i)
                coeffs.append(sympy.expand(c_i))
            
            # Evaluate p_A(A) = c_0 A^n + c_1 A^{n-1} + ... + c_n I
            p_A = zeros(n, n)
            for i, coeff in enumerate(coeffs):
                power = deg - i
                A_pow = witness**power
                term = zeros(n, n)
                for r in range(n):
                    for c_idx in range(n):
                        # Scalar multiplication from the left
                        term[r, c_idx] = sympy.expand(coeff * A_pow[r, c_idx])
                p_A = p_A + term
            
            # Check if p_A(A) is the zero matrix
            is_zero = True
            for r in range(n):
                for c_idx in range(n):
                    if sympy.expand(p_A[r, c_idx]) != 0:
                        is_zero = False
                        break
                if not is_zero:
                    break
            
            neg_Q = not is_zero
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: p_A(x) is the characteristic polynomial of A",
    "¬Q: p_A(A) != 0_{n x n}"
]
N_HYP = 2
NEG_Q_INDEX = 2