import sympy
from sympy import minimal_polynomial, factor_list, Poly
from sympy.abc import x
from sympy import QQ, I, sqrt, Rational, Integer

# Top-level setup for FieldTheory
# K and L will be constructed dynamically from the witness generators.
# The witness should be a tuple: (K_gens, L_gens, f)
# where K_gens and L_gens are lists of algebraic generators over QQ,
# and f is a polynomial expression in x.

def conditions(witness) -> list[bool]:
    try:
        K_gens, L_gens, f = witness
        K_gens = list(K_gens)
        L_gens = list(L_gens)
    except Exception:
        return [False, False, False]

    def check_H1():
        try:
            L_field = QQ.algebraic_field(*L_gens)
            # Check K is a subfield of L
            for g in K_gens:
                L_field.from_expr(g)
            
            K_field = QQ.algebraic_field(*K_gens)
            # Check f is a polynomial with coefficients in K
            p = Poly(f, x, domain=K_field)
            if p.is_zero:
                return False
            
            # Check L/K is a normal extension
            # For each generator of L, its minimal polynomial over K must split completely in L
            for g in L_gens:
                mg = minimal_polynomial(g, x)
                factors_K = factor_list(mg, x, domain=K_field)[1]
                mg_K = None
                for fac, mult in factors_K:
                    val = fac.subs(x, g)
                    if sympy.simplify(val) == 0:
                        mg_K = fac
                        break
                
                if mg_K is None:
                    return False
                    
                factors_L = factor_list(mg_K, x, domain=L_field)[1]
                for fac, mult in factors_L:
                    if Poly(fac, x).degree() > 1:
                        return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            L_field = QQ.algebraic_field(*L_gens)
            factors_L = factor_list(f, x, domain=L_field)[1]
            # f has a root in L iff it has at least one linear factor over L
            for fac, mult in factors_L:
                if Poly(fac, x).degree() == 1:
                    return True
            return False
        except Exception:
            return False

    def check_neg_Q():
        try:
            L_field = QQ.algebraic_field(*L_gens)
            factors_L = factor_list(f, x, domain=L_field)[1]
            # f does not split completely iff it has at least one irreducible factor of degree > 1
            for fac, mult in factors_L:
                if Poly(fac, x).degree() > 1:
                    return True
            return False
        except Exception:
            return False

    return [check_H1(), check_H2(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: L/K is a normal field extension",
    "H_2: f(x) has at least one root in L",
    "¬Q: f(x) does not split completely into linear factors over L"
]

N_HYP = 2
NEG_Q_INDEX = 2