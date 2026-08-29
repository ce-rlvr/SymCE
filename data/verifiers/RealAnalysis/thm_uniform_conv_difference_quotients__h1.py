import sympy as sp

# Top-level setup
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness is expected to be a tuple (f, h) where:
      - f is a sympy expression in terms of x
      - h is a sympy expression in terms of n representing the sequence h_n
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f, h = witness
    except Exception:
        return [False, False, False]
        
    # H_1: f'' is bounded on R
    try:
        f_prime = sp.diff(f, x)
        f_pprime = sp.diff(f_prime, x)
        
        h1_ok = False
        if f_pprime.is_constant():
            h1_ok = True
        else:
            try:
                rng = sp.calculus.util.function_range(f_pprime, x, sp.S.Reals)
                # If the range is a subset of real numbers, it is bounded
                h1_ok = rng.inf.is_real and rng.sup.is_real
            except Exception:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: h_n is a sequence of non-zero real numbers such that lim_{n->oo} h_n = 0
    try:
        h2_ok = False
        if not h.is_zero:
            lim_h = sp.limit(h, n, sp.oo)
            if lim_h == 0:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: D_n(x) does NOT converge uniformly to f'(x) on R
    # Uniform convergence to f'(x) means sup_{x} |D_n(x) - f'(x)| -> 0 as n -> oo.
    try:
        neg_q = False
        D_n = (f.subs(x, x + h) - f) / h
        E_n = sp.simplify(D_n - f_prime)
        
        if E_n != 0:
            # 1. Check limits at infinity
            for limit_point in [sp.oo, -sp.oo]:
                try:
                    L = sp.limit(E_n, x, limit_point)
                    if L != 0 and L != sp.nan:
                        if L == sp.oo or L == -sp.oo or L.has(sp.oo) or L.has(-sp.oo):
                            neg_q = True
                            break
                        L_n = sp.limit(L, n, sp.oo)
                        if L_n != 0:
                            neg_q = True
                            break
                except Exception:
                    pass
            
            if not neg_q:
                # 2. Test specific sequences for x that might escape to infinity or track peaks
                test_points = [n, n**2, 1/h, 1/(h**2), sp.S(0), h, -h, h**2, h**3]
                for tp in test_points:
                    try:
                        val = E_n.subs(x, tp)
                        lim_val = sp.limit(val, n, sp.oo)
                        if lim_val != 0 and lim_val != sp.nan:
                            neg_q = True
                            break
                    except Exception:
                        continue
                        
            if not neg_q:
                # 3. Try finding critical points to locate the supremum
                try:
                    dE = sp.diff(E_n, x)
                    # Only attempt to solve if it's relatively simple to avoid hanging
                    if not dE.has(sp.sin, sp.cos, sp.tan, sp.exp, sp.log):
                        crit_points = sp.solve(dE, x)
                        for cp in crit_points:
                            if cp.has(n):
                                val = E_n.subs(x, cp)
                                lim_val = sp.limit(val, n, sp.oo)
                                if lim_val != 0:
                                    neg_q = True
                                    break
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f'' is bounded on R",
    "H_2: h_n is a sequence of non-zero real numbers converging to 0",
    "¬Q: D_n(x) does not converge uniformly to f'(x) on R"
]

N_HYP = 2
NEG_Q_INDEX = 2