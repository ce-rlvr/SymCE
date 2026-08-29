import sympy
from sympy import ZZ, QQ, RR, CC, S, Symbol, degree, oo

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: The degree of f(x) is n",
    "¬Q: The polynomial f(x) has more than n distinct roots in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            f = witness.get('f')
            x = witness.get('x')
            n = witness.get('n')
            roots = witness.get('roots', [])
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 5:
                R, f, x, n, roots = witness[:5]
            elif len(witness) == 4:
                R, f, n, roots = witness
                x = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        f_expr = sympy.sympify(f)
        
        if x is None:
            free = f_expr.free_symbols
            if free:
                x = list(free)[0]
            else:
                x = Symbol('x')
        else:
            x = sympy.sympify(x)

        if isinstance(n, str):
            if n in ('-oo', '-infinity'):
                n = -oo
            else:
                n = sympy.sympify(n)
        else:
            n = sympy.sympify(n)

        roots = list(roots)

        # H_1: R is an integral domain
        h1 = False
        try:
            valid_sets = (ZZ, QQ, RR, CC, S.Integers, S.Rationals, S.Reals, S.Complexes)
            if R in valid_sets:
                h1 = True
            elif hasattr(R, 'is_Field') and R.is_Field:
                h1 = True
            elif hasattr(R, 'mod'):
                from sympy.ntheory import isprime
                h1 = isprime(R.mod)
            elif hasattr(R, 'is_IntegralDomain') and R.is_IntegralDomain:
                h1 = True
            elif isinstance(R, str) and R in ['ZZ', 'QQ', 'RR', 'CC', 'Integers', 'Rationals', 'Reals', 'Complexes']:
                h1 = True
        except Exception:
            h1 = False

        # H_2: The degree of f(x) is n
        h2 = False
        try:
            deg = degree(f_expr, x)
            h2 = bool(deg == n)
        except Exception:
            h2 = False

        # ¬Q: f(x) has more than n distinct roots in R
        neg_q = False
        try:
            if len(set(roots)) == len(roots) and bool(len(roots) > n):
                all_valid = True
                for r in roots:
                    val = f_expr.subs(x, r)
                    if hasattr(R, 'mod'):
                        if val % R.mod != 0:
                            all_valid = False
                            break
                    else:
                        val_simp = sympy.simplify(val)
                        if val_simp != 0 and not val_simp.is_zero:
                            all_valid = False
                            break
                if all_valid:
                    neg_q = True
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(neg_q)]

    except Exception:
        return [False, False, False]