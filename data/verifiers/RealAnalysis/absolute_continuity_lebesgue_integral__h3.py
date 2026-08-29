import sympy as sp

def conditions(witness) -> list[bool]:
    try:
        f = None
        domain = None
        epsilon = None
        
        if isinstance(witness, dict):
            f = witness.get('f')
            domain = witness.get('domain', witness.get('X'))
            epsilon = witness.get('epsilon')
        elif isinstance(witness, tuple) and len(witness) == 3:
            f, domain, epsilon = witness
            
        h1 = False
        if isinstance(domain, tuple) and len(domain) == 3:
            var, a, b = domain
            if isinstance(var, sp.Symbol):
                h1 = True
            
        h2 = False
        if h1 and f is not None:
            var, a, b = domain
            try:
                f_sym = sp.sympify(f)
                integral = sp.integrate(sp.Abs(f_sym), (var, a, b))
                
                if getattr(integral, 'is_finite', False) == True:
                    h2 = True
                else:
                    try:
                        if float(integral) < float('inf'):
                            h2 = True
                    except Exception:
                        pass
            except Exception:
                pass
                
        neg_q = False
        if epsilon is not None:
            try:
                if float(epsilon) <= 0:
                    neg_q = True
            except Exception:
                pass
                
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: (X, \\Sigma, \\mu) is a measure space",
    "H_2: f is an integrable function on X",
    "\\neg Q: Conclusion fails (\\epsilon <= 0 makes the strict inequality impossible for all sets)"
]

N_HYP = 2
NEG_Q_INDEX = 2