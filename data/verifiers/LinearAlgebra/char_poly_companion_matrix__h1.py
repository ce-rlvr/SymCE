import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        C, p = witness
    except Exception:
        return [False, False]
    
    # H_1: C is the n x n companion matrix associated with p(x)
    try:
        if isinstance(p, sympy.Poly):
            poly_p = p
        else:
            poly_p = sympy.Poly(p)
            
        if len(poly_p.gens) != 1:
            h1 = False
        else:
            n = poly_p.degree()
            if n < 1:
                h1 = False
            else:
                C_mat = sympy.Matrix(C)
                if C_mat.shape != (n, n):
                    h1 = False
                else:
                    coeffs = poly_p.all_coeffs()
                    c_n = coeffs[0]
                    # b contains the coefficients of the monic polynomial, negated and reversed
                    b = [-c / c_n for c in coeffs[1:]]
                    b.reverse()
                    
                    # M1: right column, subdiagonal 1s
                    M1 = sympy.zeros(n, n)
                    for i in range(n-1): M1[i+1, i] = 1
                    for i in range(n): M1[i, n-1] = b[i]
                    
                    # M2: bottom row, superdiagonal 1s
                    M2 = sympy.zeros(n, n)
                    for i in range(n-1): M2[i, i+1] = 1
                    for j in range(n): M2[n-1, j] = b[j]
                    
                    # M3: left column, superdiagonal 1s
                    M3 = sympy.zeros(n, n)
                    for i in range(n-1): M3[i, i+1] = 1
                    for i in range(n): M3[i, 0] = b[n-1-i]
                    
                    # M4: top row, subdiagonal 1s
                    M4 = sympy.zeros(n, n)
                    for i in range(n-1): M4[i+1, i] = 1
                    for j in range(n): M4[0, j] = b[n-1-j]
                    
                    def mat_eq(A, B):
                        diff_mat = A - B
                        for i in range(n):
                            for j in range(n):
                                val = diff_mat[i, j]
                                if sympy.expand(val) != 0 and sympy.simplify(val) != 0:
                                    return False
                        return True
                    
                    h1 = mat_eq(C_mat, M1) or mat_eq(C_mat, M2) or mat_eq(C_mat, M3) or mat_eq(C_mat, M4)
    except Exception:
        h1 = False

    # neg_Q: The characteristic polynomial of C is NOT exactly p(x)
    try:
        if isinstance(p, sympy.Poly):
            poly_p = p
        else:
            poly_p = sympy.Poly(p)
            
        gen = poly_p.gens[0]
        C_mat = sympy.Matrix(C)
        char_poly_expr = C_mat.charpoly(gen).as_expr()
        p_expr = poly_p.as_expr()
        
        diff = char_poly_expr - p_expr
        if sympy.expand(diff) != 0 and sympy.simplify(diff) != 0:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: C is the n x n companion matrix associated with p(x)",
    "¬Q: The characteristic polynomial of C is not exactly p(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1