import sympy
import itertools

x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = sympy.symbols('x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 5:
            p, q, n, polys, N_wit = witness
        elif len(witness) == 4:
            if isinstance(witness[1], int) and isinstance(witness[2], int) and isinstance(witness[3], (list, tuple)):
                p, q, n, polys = witness
                N_wit = None
            else:
                p, n, polys, N_wit = witness
                q = p
        elif len(witness) == 3:
            p, n, polys = witness
            q = p
            N_wit = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = sympy.isprime(p) and (q == p)
    except Exception:
        h1 = False

    try:
        if isinstance(n, int) and n > 0 and isinstance(polys, (list, tuple)) and len(polys) > 0:
            variables = [sympy.Symbol(f'x{i}') for i in range(1, n + 1)]
            h2 = True
            for poly in polys:
                try:
                    poly_expr = sympy.sympify(poly)
                    if not poly_expr.free_symbols.issubset(set(variables)):
                        h2 = False
                        break
                    if not poly_expr.is_polynomial(*variables) and not poly_expr.is_number:
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            if p**n > 100000:
                h3 = False
            else:
                N = 0
                variables = [sympy.Symbol(f'x{i}') for i in range(1, n + 1)]
                for pt in itertools.product(range(p), repeat=n):
                    is_zero = True
                    for poly in polys:
                        poly_expr = sympy.sympify(poly)
                        val = poly_expr.subs(dict(zip(variables, pt)))
                        try:
                            val_int = int(val)
                            if val_int != val:
                                is_zero = False
                                break
                            if val_int % p != 0:
                                is_zero = False
                                break
                        except TypeError:
                            is_zero = False
                            break
                    if is_zero:
                        N += 1
                
                if N_wit is None:
                    h3 = True
                else:
                    h3 = (N == N_wit)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if h1 and h2 and h3:
            neg_q = (N % p != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p",
    "H_2: f_1, ..., f_k are polynomials over F_q",
    "H_3: N is the number of common zeros of f_1, ..., f_k in F_q^n",
    "not Q: N is not divisible by p"
]

N_HYP = 3
NEG_Q_INDEX = 3