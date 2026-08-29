import sympy
import itertools
from sympy import symbols
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, dict):
            F = witness.get('F', witness.get('p', None))
            q = witness.get('q', None)
            n = witness.get('n', None)
            polys = witness.get('polys', None)
            vars = witness.get('vars', None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 5:
                F, q, n, polys, vars = witness
            elif len(witness) == 4:
                F, q, n, polys = witness
                vars = None
            else:
                return [False] * 4
        else:
            return [False] * 4

        if F is None or q is None or n is None or not polys:
            return [False] * 4

        n = int(n)
        q = int(q)
        polys = [sympy.sympify(p_expr) for p_expr in polys]

        if vars is not None:
            vars = [sympy.sympify(v) for v in vars]
        else:
            free_syms = set()
            for poly in polys:
                free_syms.update(poly.free_symbols)
            vars = sorted(list(free_syms), key=lambda s: s.name)
            if len(vars) < n:
                extra = sympy.symbols(f'extra0:{n - len(vars)}')
                vars.extend(extra)

        # Extract field characteristic/size
        p = None
        if isinstance(F, int) or isinstance(F, sympy.Integer):
            p = int(F)
        elif hasattr(F, 'mod'):
            p = int(F.mod)
        elif hasattr(F, 'order'):
            p = int(F.order)
        elif hasattr(F, 'characteristic'):
            p = int(F.characteristic)
            if hasattr(F, 'degree') and F.degree > 1:
                p = None

    except Exception:
        return [False] * 4

    # H_1: P_1, ..., P_k are polynomials in n variables over F
    try:
        h1 = False
        if p is not None and sympy.isprime(p):
            if len(vars) == n:
                all_poly = True
                for poly in polys:
                    if not poly.is_polynomial(*vars):
                        all_poly = False
                        break
                    p_poly = sympy.poly(poly, *vars)
                    # Check if coefficients are integers (elements of Z_p)
                    if not all(c.is_integer for c in p_poly.coeffs()):
                        all_poly = False
                        break
                h1 = all_poly
    except Exception:
        h1 = False

    # H_2: The sum of the total degrees of the polynomials P_1, ..., P_k is strictly less than n
    try:
        h2 = False
        if h1:
            total_deg = 0
            for poly in polys:
                p_poly = sympy.poly(poly, *vars)
                deg = p_poly.total_degree()
                if deg == sympy.S.NegativeInfinity:
                    deg = 0
                total_deg += deg
            h2 = total_deg < n
    except Exception:
        h2 = False

    # H_3: The system of equations P_1 = ... = P_k = 0 has at least one solution in F^n
    # ¬Q: The system of equations does NOT have at least q distinct solutions in F^n
    try:
        h3 = False
        neg_q = False
        if h1:
            solutions = 0
            p_int = int(p)
            for vals in itertools.product(range(p_int), repeat=n):
                is_sol = True
                val_dict = dict(zip(vars, vals))
                for poly in polys:
                    val = poly.subs(val_dict)
                    if int(val) % p_int != 0:
                        is_sol = False
                        break
                if is_sol:
                    solutions += 1
            h3 = solutions >= 1
            neg_q = solutions < q
    except Exception:
        h3 = False
        neg_q = False

    return [h1, h2, h3, neg_q]


CONDITION_LABELS = [
    "H_1: P_1, ..., P_k are polynomials in n variables over F",
    "H_2: The sum of the total degrees of the polynomials P_1, ..., P_k is strictly less than n",
    "H_3: The system of equations P_1 = ... = P_k = 0 has at least one solution in F^n",
    "¬Q: The system of equations does NOT have at least q distinct solutions in F^n"
]

N_HYP = 3
NEG_Q_INDEX = 3