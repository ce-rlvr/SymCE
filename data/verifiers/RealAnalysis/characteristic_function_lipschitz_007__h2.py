import sympy as sp

x, t = sp.symbols('x t', real=True)

CONDITION_LABELS = [
    "H_1: X is a real-valued random variable",
    "H_2: phi(t) is the characteristic function of X",
    "not Q: phi(t) is not globally Lipschitz continuous with constant E(|X|)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], list) and isinstance(witness[1], list):
            values, probs = witness
            try:
                if sp.simplify(sum(probs) - 1) == 0 and all(p >= 0 for p in probs):
                    h1_ok = True
                h2_ok = True
                e_abs_x = sum(sp.Abs(v) * p for v, p in zip(values, probs))
                if e_abs_x == sp.oo or e_abs_x == sp.zoo or str(e_abs_x) == 'oo' or (hasattr(e_abs_x, 'has') and e_abs_x.has(sp.oo)):
                    neg_q = True
                elif hasattr(e_abs_x, 'is_finite') and e_abs_x.is_finite is False:
                    neg_q = True
            except Exception:
                pass
            return [h1_ok, h2_ok, neg_q]

        if isinstance(witness, tuple) and len(witness) == 4:
            f, x_var, a, b = witness
        elif isinstance(witness, sp.Expr):
            free = list(witness.free_symbols)
            if len(free) >= 1:
                x_vars = [s for s in free if s.name == 'x']
                x_var = x_vars[0] if x_vars else free[0]
                f = witness
                a, b = -sp.oo, sp.oo
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        try:
            integral_val = sp.integrate(f, (x_var, a, b))
            if sp.simplify(integral_val - 1) == 0:
                h1_ok = True
        except Exception:
            pass
            
        h2_ok = True
        
        try:
            is_a_neg = (a == -sp.oo) or (a < 0)
            is_b_pos = (b == sp.oo) or (b > 0)
        except Exception:
            is_a_neg = False
            is_b_pos = False
            
        try:
            if is_a_neg and is_b_pos:
                e1 = sp.integrate(-x_var * f, (x_var, a, 0))
                e2 = sp.integrate(x_var * f, (x_var, 0, b))
                e_abs_x = e1 + e2
            else:
                e_abs_x = sp.integrate(sp.Abs(x_var) * f, (x_var, a, b))
            
            if e_abs_x == sp.oo or e_abs_x == sp.zoo or str(e_abs_x) == 'oo' or str(e_abs_x) == 'zoo' or str(e_abs_x) == 'nan' or (hasattr(e_abs_x, 'has') and e_abs_x.has(sp.oo)):
                neg_q = True
            elif hasattr(e_abs_x, 'is_finite') and e_abs_x.is_finite is False:
                neg_q = True
        except Exception:
            pass
            
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q]