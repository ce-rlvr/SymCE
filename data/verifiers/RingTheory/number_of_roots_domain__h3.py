import sympy
from sympy import S, Poly, Symbol

x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f is a non-zero polynomial over R",
    "¬Q: f has more than n distinct roots in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, f, n = witness
            elif len(witness) == 2:
                f, n = witness
                R = sympy.S.Complexes
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: R is an integral domain
    h1 = False
    try:
        if R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes,
                 sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC):
            h1 = True
        elif hasattr(R, 'is_domain') and R.is_domain:
            h1 = True
        elif type(R).__name__ == 'Domain':
            h1 = True
    except Exception:
        pass

    # H2: f is a non-zero polynomial over R
    h2 = False
    try:
        f_expr = sympy.sympify(f)
        poly_f = sympy.Poly(f_expr)
        if not poly_f.is_zero:
            h2 = True
    except Exception:
        pass

    # neg_Q: f has > n distinct roots in R
    neg_q = False
    try:
        if h2:
            valid_roots = set()
            try:
                roots_dict = sympy.roots(f_expr)
                for r in roots_dict.keys():
                    valid_roots.add(r)
            except Exception:
                pass
            
            if not valid_roots:
                try:
                    roots_list = sympy.solve(f_expr)
                    for r in roots_list:
                        if isinstance(r, dict):
                            if len(r) == 1:
                                r = list(r.values())[0]
                            else:
                                continue
                        valid_roots.add(r)
                except Exception:
                    pass

            filtered_roots = set()
            for r in valid_roots:
                in_R = False
                if R in (sympy.S.Integers, sympy.ZZ):
                    if r.is_integer or r in sympy.S.Integers:
                        in_R = True
                elif R in (sympy.S.Rationals, sympy.QQ):
                    if r.is_rational or r in sympy.S.Rationals:
                        in_R = True
                elif R in (sympy.S.Reals, sympy.RR):
                    if r.is_real or r in sympy.S.Reals:
                        in_R = True
                elif R in (sympy.S.Complexes, sympy.CC):
                    in_R = True
                else:
                    in_R = True
                
                if in_R:
                    filtered_roots.add(r)
            
            if len(filtered_roots) > float(n):
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]