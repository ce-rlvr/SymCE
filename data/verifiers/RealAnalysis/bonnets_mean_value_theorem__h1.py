import sympy
from sympy import Symbol, integrate, solve

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        # Extract f, g, a, b from the witness
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, g, a, b = witness
            
        # Handle string or callable inputs
        if isinstance(f, str):
            f = sympy.sympify(f)
        elif callable(f):
            f = f(x)
            
        if isinstance(g, str):
            g = sympy.sympify(g)
        elif callable(g):
            g = g(x)
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
            
        # Ensure they are sympy expressions
        if not hasattr(f, 'free_symbols'):
            f = sympy.sympify(f)
        if not hasattr(g, 'free_symbols'):
            g = sympy.sympify(g)
            
        # Determine the variable of integration
        f_syms = f.free_symbols
        g_syms = g.free_symbols
        free_syms = {s for s in (f_syms | g_syms) if s.is_Symbol}
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        elif len(free_syms) == 0:
            sym = x
        else:
            if x in free_syms:
                sym = x
            else:
                sym = list(free_syms)[0]
                
    except Exception:
        return [False, False]

    # H1: g is an integrable real-valued function on the interval
    h1_ok = False
    try:
        a_fl = float(a)
        b_fl = float(b)
        if a_fl < b_fl:
            int_g = integrate(g, (sym, a, b))
            if int_g.is_real or isinstance(int_g, (int, float, sympy.Number)):
                h1_ok = True
            else:
                # Try to evaluate to float to confirm it's a finite real number
                float(int_g)
                h1_ok = True
    except Exception:
        pass

    # neg_Q: There is NO c in the interval such that integral of f*g equals f(a) * integral of g from a to c
    neg_q_ok = False
    try:
        c = Symbol('c', real=True)
        L = integrate(f * g, (sym, a, b))
        fa = f.subs(sym, a)
        
        valid_points = [a, b]
        
        # Find critical points of R(c) = f(a) * \int_a^c g(x) dx
        # R'(c) = f(a) * g(c) = 0 => g(c) = 0
        try:
            crit_points = solve(g.subs(sym, c), c)
            for pt in crit_points:
                if pt.is_real or pt.is_real is None:
                    pt_fl = float(pt)
                    if a_fl <= pt_fl <= b_fl:
                        valid_points.append(pt)
        except Exception:
            pass

        # Sample points to ensure robustness
        for i in range(21):
            valid_points.append(a_fl + (b_fl - a_fl) * i / 20.0)

        vals = []
        G = integrate(g, sym)
        
        # Evaluate R(c) at all valid points
        if not G.has(sympy.Integral):
            # Fast evaluation using indefinite integral
            Ga = G.subs(sym, a)
            for pt in valid_points:
                try:
                    val = float(fa * (G.subs(sym, pt) - Ga))
                    if val == val:  # Check for NaN
                        vals.append(val)
                except Exception:
                    pass
        else:
            # Fallback to definite integral
            for pt in valid_points:
                try:
                    val = float(fa * integrate(g, (sym, a, pt)))
                    if val == val:
                        vals.append(val)
                except Exception:
                    pass
                    
        if vals:
            min_val = min(vals)
            max_val = max(vals)
            L_float = float(L)
            
            # If L is strictly outside the range of R(c), no such c exists
            if L_float < min_val - 1e-7 or L_float > max_val + 1e-7:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: g is an integrable real-valued function on the interval", "¬Q: There is no c such that the integral of f g equals f(a) times the integral of g"]
N_HYP = 1
NEG_Q_INDEX = 1