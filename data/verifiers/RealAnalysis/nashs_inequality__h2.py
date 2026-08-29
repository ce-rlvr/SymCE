import sympy as sp

# Top-level setup for potential witness expressions
x, y, z = sp.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the integrability/smoothness hypotheses (e.g., f in L^1 \cap H^1)
    and claims the Nash inequality holds for any function.
    
    Expected witness format:
      (n, f, vars)  where n is an integer, f is a sympy expression, vars is a tuple of variables.
      or (n, f)
      or f
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            n = witness[0]
            f = sp.sympify(witness[1])
            vars = witness[2]
        elif isinstance(witness, tuple) and len(witness) == 2:
            n = witness[0]
            f = sp.sympify(witness[1])
            vars = tuple(f.free_symbols)
        else:
            f = sp.sympify(witness)
            vars = tuple(f.free_symbols)
            n = max(1, len(vars))
            
        if not vars and isinstance(n, int) and n >= 1:
            vars = sp.symbols(f'x1:{n+1}')
            
    except Exception:
        return [False, False]

    # H_1: n >= 1 is an integer
    try:
        h1_ok = isinstance(n, int) and n >= 1
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion FAILS at the witness.
    # Conclusion: Exists C_n > 0 such that A <= C_n * B * D
    # where A = (int |f|^2)^{1 + 2/n}, B = (int |f|)^{4/n}, D = int |\nabla f|^2
    # The conclusion fails if for all C_n > 0, the inequality is false.
    # This happens if A > 0 and D = 0 (so B*D = 0 or nan, making A <= C_n * B * D false),
    # or if A = oo and B*D < oo.
    try:
        if not h1_ok:
            neg_q_ok = False
        elif f == 0:
            # If f is identically zero, A = 0, B = 0, D = 0. 
            # 0 <= C_n * 0 is True, so conclusion holds (neg_Q is False).
            neg_q_ok = False
        else:
            # Compute the integrals over R^n
            A_val = sp.integrate(sp.Abs(f)**2, *[(v, -sp.oo, sp.oo) for v in vars])
            B_val = sp.integrate(sp.Abs(f), *[(v, -sp.oo, sp.oo) for v in vars])
            
            grad_sq = sum(sp.Abs(sp.diff(f, v))**2 for v in vars)
            if grad_sq == 0:
                D_val = 0
            else:
                D_val = sp.integrate(grad_sq, *[(v, -sp.oo, sp.oo) for v in vars])
                
            if A_val == 0:
                neg_q_ok = False
            elif D_val == 0:
                # If D = 0 and A > 0, then B*D is 0 (or nan if B=oo).
                # In either case, A <= C_n * B * D is False for all C_n > 0.
                neg_q_ok = True
            elif A_val == sp.oo:
                # If A = oo, the inequality A <= C_n * B * D fails unless B*D = oo.
                if B_val == sp.oo or D_val == sp.oo:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
            else:
                # A is finite and > 0.
                if B_val == 0 or D_val == 0:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "¬Q: The inequality fails for all C_n > 0"
]

N_HYP = 1
NEG_Q_INDEX = 1