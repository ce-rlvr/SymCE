import sympy as sp
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            k = witness.get('k')
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, k = witness
        else:
            f = witness
            k = 1
    except Exception:
        return [False, False, False]

    try:
        if isinstance(f, sp.Poly):
            var = f.gen
            expr = f.as_expr()
            is_z = expr.is_zero
            if is_z is None:
                is_z = (sp.simplify(expr) == 0)
            h1 = not is_z
        else:
            expr = sp.sympify(f)
            if x in expr.free_symbols:
                var = x
            elif expr.free_symbols:
                var = list(expr.free_symbols)[0]
            else:
                var = x
            
            if isinstance(expr, sp.MatrixBase):
                is_z = expr.is_zero
                if is_z is None:
                    is_z = all(sp.simplify(e) == 0 for e in expr)
                h1 = not is_z and all(e.is_polynomial(var) for e in expr)
            else:
                is_z = expr.is_zero
                if is_z is None:
                    is_z = (sp.simplify(expr) == 0)
                h1 = not is_z and expr.is_polynomial(var)
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(k, (int, sp.Integer)):
            h2 = k >= 1
        elif hasattr(k, 'is_integer') and k.is_integer:
            h2 = k >= 1
        elif isinstance(k, float) and k.is_integer():
            h2 = k >= 1
    except Exception:
        h2 = False

    try:
        if isinstance(expr, sp.MatrixBase):
            c_f = sp.S.Zero
            for e in expr:
                if e != 0:
                    c_f = sp.gcd(c_f, sp.Poly(e, var).content())
            
            expr_xf = var**k * expr
            c_xf = sp.S.Zero
            for e in expr_xf:
                if e != 0:
                    c_xf = sp.gcd(c_xf, sp.Poly(e, var).content())
        else:
            if isinstance(f, sp.Poly):
                poly_f = f
                domain = f.domain
                poly_xf = sp.Poly(var**k * expr, var, domain=domain)
            else:
                poly_f = sp.Poly(expr, var)
                poly_xf = sp.Poly(var**k * expr, var)
            
            c_f = poly_f.content()
            c_xf = poly_xf.content()
        
        def divides(a, b):
            if a == b:
                return True
            if a == 0:
                return b == 0
            if hasattr(a, 'divides'):
                return a.divides(b)
            try:
                if isinstance(a, (int, sp.Integer)) and isinstance(b, (int, sp.Integer)):
                    return b % a == 0
            except Exception:
                pass
            try:
                q_div, r_div = sp.div(b, a)
                if r_div == 0:
                    return True
            except Exception:
                pass
            try:
                ratio = sp.cancel(b / a)
                if sp.denom(ratio) == 1:
                    return True
            except Exception:
                pass
            return False

        q = divides(c_f, c_xf) and divides(c_xf, c_f)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial",
    "H_2: k >= 1 is an integer",
    "¬Q: The content of x^k f(x) is not associate to the content of f(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2