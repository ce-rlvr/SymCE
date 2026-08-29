import sympy
import math

# Top-level setup
x, t = sympy.symbols('x t', real=True)

CONDITION_LABELS = [
    "H_1: f is a continuous function on the domain",
    "¬Q: F is NOT Lipschitz continuous with constant L(d - c)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    step = (stop - start) / (n - 1)
    for i in range(n):
        yield start + step * i

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
            L = witness['L']
        else:
            f, a, b, c, d, L = witness
    except Exception:
        return [False, False]

    # H_1: f is continuous on [a, b] x [c, d]
    h1_ok = False
    try:
        a_f, b_f, c_f, d_f = float(a), float(b), float(c), float(d)
        if a_f > b_f or c_f > d_f:
            h1_ok = False
        else:
            is_cont = True
            try:
                f_lam = sympy.lambdify((x, t), f, modules=['math', {'Abs': abs}])
                for xv in linspace(a_f, b_f, 20):
                    for tv in linspace(c_f, d_f, 20):
                        val = f_lam(xv, tv)
                        if isinstance(val, complex):
                            is_cont = False
                            break
                        try:
                            if math.isnan(float(val)) or math.isinf(float(val)):
                                is_cont = False
                                break
                        except Exception:
                            is_cont = False
                            break
                    if not is_cont:
                        break
            except Exception:
                # Fallback to subs
                for xv in linspace(a_f, b_f, 10):
                    for tv in linspace(c_f, d_f, 10):
                        val = f.subs({x: xv, t: tv}).evalf()
                        if not val.is_real or not val.is_finite:
                            is_cont = False
                            break
                    if not is_cont:
                        break
            h1_ok = is_cont
    except Exception:
        h1_ok = False

    # neg_Q: F(x) is NOT Lipschitz continuous with constant L(d - c)
    neg_q_ok = False
    try:
        a_f, b_f, c_f, d_f, L_f = float(a), float(b), float(c), float(d), float(L)
        target = L_f * (d_f - c_f)
        
        found_violation = False
        
        try:
            # Numerical integration using lambdify
            f_lam = sympy.lambdify((x, t), f, modules=['math', {'Abs': abs}])
            xs = list(linspace(a_f, b_f, 50))
            Fs = []
            for xv in xs:
                n_steps = 50
                step = (d_f - c_f) / n_steps
                s = f_lam(xv, c_f) + f_lam(xv, d_f)
                for k in range(1, n_steps):
                    tv = c_f + k * step
                    weight = 4 if k % 2 != 0 else 2
                    s += weight * f_lam(xv, tv)
                Fs.append(float(s) * step / 3)
                
            for i in range(len(xs)):
                for j in range(i+1, len(xs)):
                    dx = abs(xs[i] - xs[j])
                    if dx > 1e-12:
                        dq = abs(Fs[i] - Fs[j]) / dx
                        if dq > target + 1e-4:
                            found_violation = True
                            break
                if found_violation:
                    break
        except Exception:
            # Fallback to numerical integration using subs
            xs = list(linspace(a_f, b_f, 20))
            Fs = []
            for xv in xs:
                n_steps = 20
                step = (d_f - c_f) / n_steps
                s = f.subs({x: xv, t: c_f}).evalf() + f.subs({x: xv, t: d_f}).evalf()
                for k in range(1, n_steps):
                    tv = c_f + k * step
                    weight = 4 if k % 2 != 0 else 2
                    s += weight * f.subs({x: xv, t: tv}).evalf()
                Fs.append(s * step / 3)
                
            for i in range(len(xs)):
                for j in range(i+1, len(xs)):
                    dx = abs(xs[i] - xs[j])
                    if dx > 1e-12:
                        dq = abs(Fs[i] - Fs[j]) / dx
                        if dq > target + 1e-4:
                            found_violation = True
                            break
                if found_violation:
                    break
                    
        neg_q_ok = found_violation
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]