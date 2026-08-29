import sympy
from sympy import Poly, Matrix, QQ
from sympy.abc import x

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F')
        E = witness.get('E')
        alpha = witness.get('alpha')
        m = witness.get('m')
        x_var = witness.get('x', x)
    else:
        F = getattr(witness, 'F', None)
        E = getattr(witness, 'E', None)
        alpha = getattr(witness, 'alpha', None)
        m = getattr(witness, 'm', None)
        x_var = getattr(witness, 'x', x)

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        h2 = bool(E.is_Field and F.unify(E) == E)
    except Exception:
        h2 = False

    try:
        if not isinstance(m, Poly) or m.gen != x_var or m.domain != F:
            h3 = False
        elif m.LC() != 1:
            h3 = False
        else:
            if isinstance(alpha, Matrix):
                min_p_expr = alpha.minimal_polynomial(x_var)
                min_p = Poly(min_p_expr, x_var, domain=F)
                h3 = bool(m == min_p)
            else:
                from sympy import minpoly, simplify
                min_p_expr = minpoly(alpha, x_var)
                if F == QQ:
                    min_p = Poly(min_p_expr, x_var, domain=F)
                    h3 = bool(m == min_p)
                else:
                    if not m.is_irreducible:
                        h3 = False
                    else:
                        val = simplify(m.eval(alpha))
                        h3 = bool(val == 0 or val.is_zero)
    except Exception:
        h3 = False

    try:
        is_irred_E = bool(m.set_domain(E).is_irreducible)
        
        def degree_over(a, K):
            if isinstance(a, Matrix):
                return Poly(a.minimal_polynomial(x_var), x_var).degree()
            else:
                from sympy import minpoly, simplify
                if K == QQ:
                    return Poly(minpoly(a, x_var), x_var).degree()
                else:
                    p = Poly(minpoly(a, x_var), x_var, domain=K)
                    factors = p.factor_list()[1]
                    for factor, _ in factors:
                        val = simplify(factor.eval(a))
                        if val == 0 or val.is_zero:
                            return factor.degree()
                    return p.degree()
        
        deg_E = degree_over(alpha, E)
        deg_F = degree_over(alpha, F)
        
        conclusion = (is_irred_E == (deg_E == deg_F))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "¬Q: m(x) is irreducible over E iff degree of E(alpha) over E equals degree of F(alpha) over F fails"
]

N_HYP = 3
NEG_Q_INDEX = 3