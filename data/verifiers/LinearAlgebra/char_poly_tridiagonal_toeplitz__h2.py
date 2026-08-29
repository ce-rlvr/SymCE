import sympy
import math
import itertools
import functools

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            n, a, b, c, A = witness
        elif isinstance(witness, dict):
            n = witness['n']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            A = witness['A']
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: n is a positive integer
    try:
        h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False

    # H2: b != 0
    try:
        b_simp = sympy.simplify(b)
        if b_simp == 0:
            h2 = False
        else:
            if hasattr(b_simp, 'free_symbols') and len(b_simp.free_symbols) > 0:
                h2 = True
            else:
                h2 = abs(complex(b_simp)) > 1e-9
    except Exception:
        h2 = False

    # H3: c != 0
    try:
        c_simp = sympy.simplify(c)
        if c_simp == 0:
            h3 = False
        else:
            if hasattr(c_simp, 'free_symbols') and len(c_simp.free_symbols) > 0:
                h3 = True
            else:
                h3 = abs(complex(c_simp)) > 1e-9
    except Exception:
        h3 = False

    # Conclusion: The roots of the characteristic polynomial of A are given by the formula
    try:
        if not (hasattr(A, 'shape') and hasattr(A, 'charpoly')):
            q = False
        elif A.shape != (n, n):
            q = False
        else:
            x_sym = sympy.Symbol('x_sym_var')
            char_poly_expr = A.charpoly(x_sym).as_expr()
            q = True
            for k in range(1, int(n) + 1):
                lam_k = a + 2 * sympy.sqrt(b * c) * sympy.cos(k * sympy.pi / (n + 1))
                val = char_poly_expr.subs(x_sym, lam_k)
                val_simp = sympy.simplify(val)
                if val_simp != 0:
                    if hasattr(val_simp, 'free_symbols') and len(val_simp.free_symbols) > 0:
                        q = False
                        break
                    else:
                        try:
                            if abs(complex(val_simp)) > 1e-9:
                                q = False
                                break
                        except Exception:
                            q = False
                            break
    except Exception:
        q = False

    neg_q = not q

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: b != 0",
    "H_3: c != 0",
    "¬Q: The roots of the characteristic polynomial of A are NOT given by the formula"
]

N_HYP = 3
NEG_Q_INDEX = 3