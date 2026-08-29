import sympy
from sympy import limit, Symbol, S

# Top-level setup: define the symbol that the witness expression will use.
# The witness is expected to be a sympy expression in terms of x,
# representing a function f: R -> R.
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: G and H are topological groups equipped with left-invariant metrics",
    "H_2: f is continuous at the identity element of G",
    "¬Q: f is not uniformly continuous on G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: G and H are topological groups equipped with left-invariant metrics.
    # We implicitly use G = H = R with addition and the standard metric.
    # We just check if the witness is a valid sympy expression.
    try:
        h1 = isinstance(witness, sympy.Expr)
    except Exception:
        h1 = False

    # H_2: f is continuous at the identity element of G (which is 0).
    try:
        if not h1:
            h2 = False
        else:
            f_0 = witness.subs(x, 0)
            lim_0 = limit(witness, x, 0)
            
            # Ensure the value at 0 is a finite real number
            try:
                float(f_0)
                is_fin = True
            except Exception:
                is_fin = False
                
            h2 = (f_0 == lim_0) and is_fin
    except Exception:
        h2 = False

    # ¬Q: The homomorphism f is not uniformly continuous on G.
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = False
            n = Symbol('n', real=True, positive=True)
            
            # Method 1: Check if the limit of |f(n + 1/n) - f(n)| as n -> oo is strictly greater than 0.
            # If f is uniformly continuous, this limit must be 0.
            try:
                diff_expr = witness.subs(x, n + 1/n) - witness.subs(x, n)
                L = limit(abs(diff_expr), n, sympy.oo)
                if L.is_extended_real and L > 0:
                    neg_q = True
            except Exception:
                pass
            
            # Method 2: Check if the limit of |f'(x)| as x -> oo is infinity.
            # If the derivative is unbounded in this way, f is not uniformly continuous.
            if not neg_q:
                try:
                    deriv = witness.diff(x)
                    L_deriv = limit(abs(deriv), x, sympy.oo)
                    if L_deriv == sympy.oo:
                        neg_q = True
                except Exception:
                    pass
            
            # Method 3: Heuristic for oscillating unbounded derivatives (e.g., sin(x**2)).
            if not neg_q:
                try:
                    deriv = witness.diff(x)
                    L_deriv = limit(abs(deriv), x, sympy.oo)
                    
                    # If we can prove the derivative is bounded at infinity, it is uniformly continuous.
                    if L_deriv != sympy.oo and L_deriv.is_extended_real:
                        pass
                    else:
                        max_d = []
                        # Sample the derivative at exponentially increasing magnitudes
                        for base in [10, 100, 1000, 10000]:
                            samples = []
                            for i in range(5):
                                try:
                                    val = abs(float(deriv.subs(x, base + i)))
                                    samples.append(val)
                                except Exception:
                                    pass
                            if samples:
                                max_d.append(max(samples))
                        
                        # If the derivative's magnitude is strictly and significantly increasing,
                        # it is unbounded, hence f is not uniformly continuous.
                        if len(max_d) >= 4:
                            increasing = True
                            sustained_growth = True
                            for i in range(1, len(max_d)):
                                if max_d[i] <= max_d[i-1]:
                                    increasing = False
                                    break
                                if max_d[i] < max_d[i-1] * 1.1:
                                    sustained_growth = False
                            if increasing and sustained_growth and max_d[-1] > max_d[0] * 1.5:
                                neg_q = True
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]