import sympy as sp

t, y = sp.symbols('t y')

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a dictionary with:
      - 'f': a sympy expression in terms of t and y
      - 't0': a float or sympy number
      - 'y0': a float or sympy number
      - 'solutions': a list of sympy expressions in terms of t representing distinct local solutions
    """
    # H1: D is an open region containing (t0, y0)
    h1 = False
    try:
        f_expr = sp.sympify(witness['f'])
        t0 = float(witness['t0'])
        y0 = float(witness['y0'])
        
        h1 = True
        # Check if f evaluates to a real number in a neighborhood of (t0, y0)
        for dt in [-0.1, 0, 0.1]:
            for dy in [-0.1, 0, 0.1]:
                val = complex(f_expr.subs({t: t0 + dt, y: y0 + dy}).evalf())
                if abs(val.imag) > 1e-9:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H2: f is continuous in the variable t
    h2 = False
    try:
        f_expr = sp.sympify(witness['f'])
        t0 = float(witness['t0'])
        y0 = float(witness['y0'])
        
        if t not in f_expr.free_symbols:
            h2 = True
        else:
            h2 = True
            # Check continuity in t at a few points around t0 for a few values of y
            for dt in [0, 0.05, -0.05]:
                for dy in [-0.1, 0, 0.1]:
                    y_val = y0 + dy
                    t_val = t0 + dt
                    f_y = f_expr.subs(y, y_val)
                    lim = sp.limit(f_y, t, t_val)
                    val = f_y.subs(t, t_val)
                    if abs(complex((lim - val).evalf())) > 1e-7:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist a unique local solution to the IVP
    # We verify this by checking if the witness provides at least 2 distinct valid local solutions.
    neg_q = False
    try:
        f_expr = sp.sympify(witness['f'])
        t0 = float(witness['t0'])
        y0 = float(witness['y0'])
        sols = witness.get('solutions', [])
        
        valid_sols = []
        for sol in sols:
            sol = sp.sympify(sol)
            # Check initial condition y(t0) == y0
            try:
                y_t0 = complex(sol.subs(t, t0).evalf())
                if abs(y_t0 - y0) > 1e-7:
                    continue
            except Exception:
                continue
            
            # Check differential equation y'(t) == f(t, y(t)) locally
            lhs = sp.diff(sol, t)
            rhs = f_expr.subs(y, sol)
            
            match = True
            for dt in [-0.1, -0.05, 0.0, 0.05, 0.1]:
                try:
                    val_lhs = complex(lhs.subs(t, t0 + dt).evalf())
                    val_rhs = complex(rhs.subs(t, t0 + dt).evalf())
                    if abs(val_lhs - val_rhs) > 1e-5:
                        match = False
                        break
                except Exception:
                    match = False
                    break
            if match:
                valid_sols.append(sol)
                
        # Check if there are at least 2 distinct valid solutions
        if len(valid_sols) >= 2:
            for i in range(len(valid_sols)):
                for j in range(i + 1, len(valid_sols)):
                    distinct = False
                    for dt in [-0.1, -0.05, 0.05, 0.1]:
                        try:
                            val_i = complex(valid_sols[i].subs(t, t0 + dt).evalf())
                            val_j = complex(valid_sols[j].subs(t, t0 + dt).evalf())
                            if abs(val_i - val_j) > 1e-7:
                                distinct = True
                                break
                        except Exception:
                            pass
                    if distinct:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: D is an open region containing (t0, y0)",
    "H_2: f is continuous in the variable t",
    "¬Q: There does not exist a unique local solution to the IVP"
]

N_HYP = 2
NEG_Q_INDEX = 2