import sympy as sp
from sympy import Poly, Matrix
from sympy.abc import x, y, z
import itertools
import math
from functools import reduce

CONDITION_LABELS = [
    "H_1: K is a number field",
    "H_2: I is a non-zero ideal of O_K",
    "H_3: J is a non-zero ideal of O_K",
    "¬Q: N(IJ) != N(I)N(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        f, I_gens, J_gens = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        f_expr = sp.sympify(f)
        free_vars = f_expr.free_symbols
        if len(free_vars) == 1:
            var = list(free_vars)[0]
        else:
            var = x
            
        f_poly = Poly(f_expr, var, domain='ZZ')
        h1 = f_poly.degree() >= 1 and f_poly.LC() == 1 and f_poly.is_irreducible
    except Exception:
        h1 = False
        var = x

    def ideal_norm(gens):
        try:
            basis_polys = []
            n = f_poly.degree()
            for g in gens:
                g_poly = Poly(g, var, domain='ZZ')
                for k in range(n):
                    term = Poly(var**k, var, domain='ZZ') * g_poly
                    _, rem = term.div(f_poly)
                    basis_polys.append(rem)
            
            rows = []
            for p in basis_polys:
                coeffs = p.all_coeffs()
                coeffs = [0]*(n - len(coeffs)) + coeffs
                rows.append([int(c) for c in coeffs])
            
            M = Matrix(rows)
            if M.shape[0] < n:
                return 0
            minors = []
            for sub_indices in itertools.combinations(range(M.shape[0]), n):
                subM = M[list(sub_indices), :]
                minors.append(int(abs(subM.det())))
            if not minors:
                return 0
            return reduce(math.gcd, minors)
        except Exception:
            return -1

    try:
        norm_I = ideal_norm(I_gens)
        h2 = norm_I > 0
    except Exception:
        h2 = False

    try:
        norm_J = ideal_norm(J_gens)
        h3 = norm_J > 0
    except Exception:
        h3 = False

    try:
        prod_gens = []
        for g1 in I_gens:
            for g2 in J_gens:
                p1 = Poly(g1, var, domain='ZZ')
                p2 = Poly(g2, var, domain='ZZ')
                _, rem = (p1 * p2).div(f_poly)
                prod_gens.append(rem.as_expr())
        
        norm_IJ = ideal_norm(prod_gens)
        neg_q = (norm_IJ != norm_I * norm_J) and (norm_I > 0) and (norm_J > 0) and (norm_IJ > 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]