import sympy
from sympy.abc import x, y
from sympy import integrate, limit, oo, diff, Abs, S

CONDITION_LABELS = ["H_1: f is a continuous function", "not Q: F is not uniformly continuous"]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            d = witness.get('d')
        elif isinstance(witness, (list, tuple)) and len(witness) == 5:
            f, a, b, c, d = witness
        else:
            return [False, False]
            
        if any(v is None for v in [f, a, b, c, d]):
            return [False, False]
            
        # Ensure a, b, c, d are valid numbers or infinities
        for val in [a, b, c, d]:
            if not (isinstance(val, (int, float)) or val in (oo, -oo) or getattr(val, 'is_number', False)):
                return [False, False]

        # H1: f is continuous on [a, b] x [c, d]
        h1_ok = False
        try:
            if hasattr(f, 'is_polynomial') and f.is_polynomial(x, y):
                h1_ok = True
            else:
                def get_pts(start, end):
                    if start == -oo and end == oo:
                        return [S(-1), S(0), S(1)]
                    elif start == -oo:
                        return [end-2, end-1, end]
                    elif end == oo:
                        return [start, start+1, start+2]
                    else:
                        return [start, start + (end-start)/4, (start+end)/2, end - (end-start)/4, end]
                
                x_pts = get_pts(a, b)
                y_pts = get_pts(c, d)
                h1_ok = True
                for xp in x_pts:
                    for yp in y_pts:
                        val = f.subs({x: xp, y: yp}).evalf()
                        if val.has(S.Infinity, S.NegativeInfinity, S.NaN, S.ComplexInfinity) or not val.is_real:
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
        except Exception:
            h1_ok = False

        # neg_Q: F is NOT uniformly continuous on [a, b]
        neg_q = False
        try:
            F = integrate(f, (y, c, d))
            
            is_unif_cont = True
            if a != -oo and b != oo:
                L_a = limit(F, x, a, dir='+')
                L_b = limit(F, x, b, dir='-')
                if L_a in (oo, -oo, S.NaN, S.ComplexInfinity) or L_b in (oo, -oo, S.NaN, S.ComplexInfinity):
                    is_unif_cont = False
                else:
                    pts = [a, a + (b-a)/4, (a+b)/2, b - (b-a)/4, b]
                    for p in pts:
                        val = F.subs(x, p).evalf()
                        if val.has(S.Infinity, S.NegativeInfinity, S.NaN, S.ComplexInfinity) or not val.is_real:
                            is_unif_cont = False
                            break
            elif hasattr(F, 'is_polynomial') and F.is_polynomial(x):
                from sympy import degree
                is_unif_cont = degree(F, x) <= 1
            else:
                dF = diff(F, x)
                if b == oo:
                    L = limit(Abs(dF), x, oo)
                    if L in (oo, S.ComplexInfinity):
                        is_unif_cont = False
                    elif hasattr(L, 'max') and L.max == oo:
                        is_unif_cont = False
                    else:
                        try:
                            pts = [10.1, 100.1, 1000.1, 10000.1, 100000.1]
                            vals = [float(Abs(dF.subs(x, p).evalf())) for p in pts]
                            if max(vals) > 10000 and max(vals) > 10 * min(vals):
                                is_unif_cont = False
                        except Exception:
                            pass
                if is_unif_cont and a == -oo:
                    L = limit(Abs(dF), x, -oo)
                    if L in (oo, S.ComplexInfinity):
                        is_unif_cont = False
                    elif hasattr(L, 'max') and L.max == oo:
                        is_unif_cont = False
                    else:
                        try:
                            pts = [-10.1, -100.1, -1000.1, -10000.1, -100000.1]
                            vals = [float(Abs(dF.subs(x, p).evalf())) for p in pts]
                            if max(vals) > 10000 and max(vals) > 10 * min(vals):
                                is_unif_cont = False
                        except Exception:
                            pass
            
            neg_q = not is_unif_cont
        except Exception:
            neg_q = False

        return [h1_ok, neg_q]
    except Exception:
        return [False, False]