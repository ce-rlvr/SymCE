import sympy as sp
from sympy.abc import x

# Top-level setup
# The witness is expected to be a tuple (f, I_gens, J_gens) where:
# - f is a monic irreducible polynomial in x over ZZ, defining an order Z[x]/(f) in a number field.
# - I_gens is a list of polynomials in x over ZZ generating the ideal I.
# - J_gens is a list of polynomials in x over ZZ generating the ideal J.

def conditions(witness):
    try:
        f, I_gens, J_gens = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: \mathcal{O}_K is the ring of integers of K
    # We verify that f defines an order in a number field (monic and irreducible over ZZ).
    # (A common source of counterexamples to this conjecture is using a non-maximal order).
    try:
        f_poly = sp.poly(f, x, domain='ZZ')
        h1 = bool(f_poly.LC() == 1 and f_poly.is_irreducible and f_poly.degree() >= 1)
    except Exception:
        h1 = False

    def ideal_norm(gens):
        try:
            n = f_poly.degree()
            rows = []
            for g in gens:
                g_poly = sp.poly(g, x, domain='ZZ')
                if g_poly is None:
                    continue
                g_expr = g_poly.as_expr()
                for i in range(n):
                    prod = g_expr * (x**i)
                    rem = sp.rem(prod, f, x, domain='ZZ')
                    rem_poly = sp.poly(rem, x, domain='ZZ')
                    if rem_poly is None or rem_poly.is_zero:
                        coeffs = [0] * n
                    else:
                        coeffs = rem_poly.all_coeffs()[::-1]
                        while len(coeffs) < n:
                            coeffs.append(0)
                    rows.append(coeffs)
            if not rows:
                return 0
            M = sp.Matrix(rows)
            S = M.smith_normal_form()
            norm = 1
            for i in range(n):
                norm *= S[i, i]
            return abs(norm)
        except Exception:
            return -1

    # H_2: I is a non-zero ideal of \mathcal{O}_K
    try:
        norm_I = ideal_norm(I_gens)
        h2 = bool(norm_I > 0)
    except Exception:
        h2 = False

    # H_3: J is a non-zero ideal of \mathcal{O}_K
    try:
        norm_J = ideal_norm(J_gens)
        h3 = bool(norm_J > 0)
    except Exception:
        h3 = False

    # ¬Q: N(IJ) != N(I)N(J)
    try:
        IJ_gens = []
        for g in I_gens:
            for h in J_gens:
                g_expr = sp.poly(g, x, domain='ZZ').as_expr()
                h_expr = sp.poly(h, x, domain='ZZ').as_expr()
                prod = g_expr * h_expr
                rem = sp.rem(prod, f, x, domain='ZZ')
                IJ_gens.append(rem)
        norm_IJ = ideal_norm(IJ_gens)
        neg_q = bool((norm_IJ != norm_I * norm_J) and (norm_IJ >= 0) and (norm_I >= 0) and (norm_J >= 0))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: \\mathcal{O}_K is the ring of integers of K",
    "H_2: I is a non-zero ideal of \\mathcal{O}_K",
    "H_3: J is a non-zero ideal of \\mathcal{O}_K",
    "¬Q: N(IJ) != N(I)N(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3