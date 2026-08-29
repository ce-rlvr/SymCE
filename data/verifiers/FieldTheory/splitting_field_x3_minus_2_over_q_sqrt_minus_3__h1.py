import sympy
from sympy import Rational, I, sqrt, minpoly
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

QQ = sympy.S.Rationals

def degree_over_QQ(gens):
    if not gens:
        return 1
    non_rat_gens = []
    for g in gens:
        g = sympy.sympify(g)
        if g.is_Rational:
            continue
        if g not in non_rat_gens:
            non_rat_gens.append(g)
    if not non_rat_gens:
        return 1
    if len(non_rat_gens) == 1:
        return minpoly(non_rat_gens[0], x).degree()
    minpoly_x, _ = primitive_element(non_rat_gens, x)
    return minpoly_x.degree()

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], list) and isinstance(witness[1], list):
            F_gens, K_gens = witness
        else:
            F_gens = witness if isinstance(witness, list) else [witness]
            K_gens = F_gens + [2**Rational(1, 3), I*sqrt(3)]
    except Exception:
        return [False, False, False]

    try:
        deg_F = degree_over_QQ(F_gens)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        deg_K = degree_over_QQ(K_gens)
        deg_target = degree_over_QQ(F_gens + [2**Rational(1, 3), I*sqrt(3)])
        deg_union = degree_over_QQ(K_gens + F_gens + [2**Rational(1, 3), I*sqrt(3)])
        h2_ok = (deg_K == deg_target) and (deg_K == deg_union)
    except Exception:
        h2_ok = False

    try:
        deg_F = degree_over_QQ(F_gens)
        deg_F_cbrt2 = degree_over_QQ(F_gens + [2**Rational(1, 3)])
        deg_union_K_F_cbrt2 = degree_over_QQ(K_gens + F_gens + [2**Rational(1, 3)])
        k_eq_f_cbrt2 = (deg_K == deg_F_cbrt2) and (deg_K == deg_union_K_F_cbrt2)
        deg_k_f_eq_3 = (deg_K == 3 * deg_F)
        conclusion = k_eq_f_cbrt2 and deg_k_f_eq_3
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) = x^3-2 in F polynomials",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: K != F(cbrt(2)) or degree of K over F != 3"
]

N_HYP = 2
NEG_Q_INDEX = 2