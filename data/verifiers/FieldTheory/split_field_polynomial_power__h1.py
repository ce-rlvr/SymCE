import sympy
from sympy import Symbol, degree, minpoly
from sympy.polys.numberfields import primitive_element

# Top-level setup
x = Symbol('x')

def get_splitting_field_degree(roots_list):
    if not roots_list:
        return 1
    alg_roots = []
    for r in roots_list:
        if hasattr(r, 'is_Rational') and r.is_Rational:
            continue
        alg_roots.append(r)
    if not alg_roots:
        return 1
    try:
        prim = primitive_element(alg_roots, ex=False)
        if isinstance(prim, tuple):
            prim = prim[0]
        mp = minpoly(prim)
        return degree(mp)
    except Exception:
        return -1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                F, f, m, K = witness
            elif len(witness) == 3:
                if isinstance(witness[2], int) or (hasattr(witness[2], 'is_integer') and (witness[2].is_integer() if callable(witness[2].is_integer) else witness[2].is_integer)):
                    F, f, m = witness
                else:
                    f, m, K = witness
            elif len(witness) == 2:
                f, m = witness
            else:
                return [False, False, False, False]
        else:
            f = witness.f
            m = witness.m

        if hasattr(f, 'as_expr'):
            f_expr = f.as_expr()
        else:
            f_expr = f
            
        x_syms = list(f_expr.free_symbols)
        if len(x_syms) == 1:
            x_var = x_syms[0]
            h1 = f_expr.is_polynomial(x_var)
        elif len(x_syms) == 0:
            x_var = Symbol('x')
            h1 = True
        else:
            h1 = False

        if isinstance(m, int):
            h2 = m >= 1
        elif hasattr(m, 'is_integer'):
            if callable(m.is_integer):
                h2 = m.is_integer() and m >= 1
            else:
                h2 = m.is_integer and m >= 1
        else:
            h2 = False

        h3 = True

        roots_f = sympy.roots(f_expr, x_var)
        
        def check_diff(r_f, r_Q):
            deg_f = get_splitting_field_degree(list(r_f.keys()))
            deg_Q = get_splitting_field_degree(list(r_Q.keys()))
            if deg_f != -1 and deg_Q != -1:
                return deg_f != deg_Q
            return set(r_f.keys()) != set(r_Q.keys())

        # Literal interpretation: (f(x))^m
        poly_Q_literal = f_expr**m
        roots_Q_literal = sympy.roots(poly_Q_literal, x_var)
        neg_q_literal = check_diff(roots_f, roots_Q_literal)
        
        # Typo interpretation: f(x^m)
        poly_Q_typo = f_expr.subs(x_var, x_var**m)
        roots_Q_typo = sympy.roots(poly_Q_typo, x_var)
        neg_q_typo = check_diff(roots_f, roots_Q_typo)
        
        # Composition interpretation: f^m(x)
        if int(m) <= 10:
            poly_Q_comp = f_expr
            for _ in range(int(m) - 1):
                poly_Q_comp = poly_Q_comp.subs(x_var, f_expr)
            roots_Q_comp = sympy.roots(poly_Q_comp, x_var)
            neg_q_comp = check_diff(roots_f, roots_Q_comp)
        else:
            neg_q_comp = False

        neg_q = neg_q_literal or neg_q_typo or neg_q_comp

        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is a polynomial over F",
    "H_2: m is an integer >= 1",
    "H_3: K is the splitting field of f over F",
    "not Q: K is not the splitting field of f^m over F"
]

N_HYP = 3
NEG_Q_INDEX = 3