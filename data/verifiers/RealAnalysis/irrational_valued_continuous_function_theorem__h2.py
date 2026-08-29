import sympy
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: f is a continuous function on the interval",
    "¬Q: f is not a constant function on the interval"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, a, b = witness
            elif len(witness) == 2:
                f, interval = witness
                a, b = interval[0], interval[1]
            else:
                f = witness[0]
                a, b = 0, 1
        else:
            f = witness
            a, b = 0, 1
            
        if isinstance(f, str):
            f = sympy.sympify(f)
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False]

    is_sympy = isinstance(f, sympy.Expr)
    var = x
    if is_sympy:
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
    
    h1 = False
    try:
        if a < b:
            if is_sympy:
                if f.is_polynomial(var):
                    h1 = True
                else:
                    try:
                        from sympy.calculus.util import continuous_domain
                        dom = continuous_domain(f, var, sympy.Interval(a, b))
                        h1 = sympy.Interval(a, b).is_subset(dom)
                    except Exception:
                        h1 = False
            else:
                h1 = True
                for pt in [a, b, a + (b-a)/2, a + (b-a)/3, a + 2*(b-a)/3]:
                    try:
                        val = f(pt)
                        s_val = sympy.sympify(val)
                        if s_val.is_real is False or s_val.is_finite is False:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    neg_q = False
    try:
        if a < b:
            if is_sympy:
                val_a = f.subs(var, a)
                val_mid = f.subs(var, a + (b-a)/sympy.S(2))
                val_b = f.subs(var, b)
                
                if sympy.simplify(val_a - val_b) != 0 or sympy.simplify(val_a - val_mid) != 0:
                    neg_q = True
                else:
                    df = sympy.diff(f, var)
                    if sympy.simplify(df) != 0:
                        neg_q = True
            else:
                pts = [a, b, a + (b-a)/2, a + (b-a)/3, a + 2*(b-a)/3, a + (b-a)/4, a + (b-a)/5]
                vals = []
                for pt in pts:
                    vals.append(f(pt))
                for i in range(len(vals)):
                    for j in range(i+1, len(vals)):
                        diff = sympy.sympify(vals[i]) - sympy.sympify(vals[j])
                        if diff != 0 and sympy.simplify(diff) != 0:
                            neg_q = True
                            break
                    if neg_q:
                        break
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]