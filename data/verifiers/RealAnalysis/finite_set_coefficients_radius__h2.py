import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup: named object bindings that the witness expression may reference.
n = Symbol('n', integer=True, nonnegative=True)
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
        expr = sympy.sympify(expr)
    except Exception:
        return [False, False, False]

    # H_1: sum a_n x^n is a power series
    # This means the sequence a_n is well-defined for n >= 0
    h1 = True
    for i in range(10):
        try:
            val = expr.subs(n, i)
            if val.has(sympy.nan) or val.has(sympy.zoo) or val.has(sympy.oo) or val.has(-sympy.oo):
                h1 = False
                break
        except Exception:
            h1 = False
            break

    # H_2: The sequence a_n is not eventually zero
    # We check if it is non-zero for some large values of n
    h2 = False
    for i in range(1000, 1010):
        try:
            val = sympy.N(expr.subs(n, i))
            if float(sympy.Abs(val)) > 1e-12:
                h2 = True
                break
        except OverflowError:
            # If it overflows float, it's definitely non-zero
            h2 = True
            break
        except Exception:
            pass

    # neg_Q: The radius of convergence of the power series is not exactly 1
    # R = 1 / limsup |a_n|^(1/n). We check if rho = limsup |a_n|^(1/n) != 1.
    neg_q = False
    try:
        rho = None
        try:
            rho = limit(Abs(expr)**(1/n), n, oo)
        except Exception:
            pass

        if rho is None or isinstance(rho, sympy.Limit) or rho.has(sympy.nan):
            try:
                rho = limit(Abs(expr.subs(n, n+1) / expr), n, oo)
            except Exception:
                pass

        if rho is None or isinstance(rho, sympy.Limit) or rho.has(sympy.nan):
            # Evaluate numerically as a fallback
            def get_v(base_n):
                val_a = sympy.N(sympy.Abs(expr.subs(n, base_n)))
                val_b = sympy.N(sympy.Abs(expr.subs(n, base_n + 1)))
                try:
                    max_val = val_a if bool(val_a > val_b) else val_b
                except Exception:
                    max_val = val_a
                return float(sympy.N(max_val ** sympy.Rational(1, base_n)))

            v1 = get_v(1000)
            v2 = get_v(5000)
            
            if abs(v1 - 1.0) < 0.02 and abs(v2 - 1.0) < 0.02:
                neg_q = False
            else:
                neg_q = True
        else:
            # rho was successfully evaluated analytically
            if rho == 1:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        # If we cannot evaluate the radius of convergence, return False
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: sum a_n x^n is a power series",
    "H_2: The sequence a_n is not eventually zero",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2