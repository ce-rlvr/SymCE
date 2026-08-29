import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x', real=True)
n = sp.Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis from Egorov's Theorem is that the limit function f 
    must be real-valued (finite) almost everywhere.
    """
    def get_attr(attr):
        if isinstance(witness, dict) and attr in witness:
            return witness[attr]
        elif hasattr(witness, attr):
            return getattr(witness, attr)
        else:
            raise ValueError(f"Missing {attr}")

    try:
        domain = get_attr('domain')
        if isinstance(domain, sp.Interval):
            a, b = domain.start, domain.end
        else:
            a, b = domain
        a = sp.sympify(a)
        b = sp.sympify(b)
        
        local_dict = {'x': x, 'n': n, 'oo': sp.oo}
        
        f_n_raw = get_attr('f_n')
        if callable(f_n_raw):
            try:
                f_n = sp.sympify(f_n_raw(n, x))
            except Exception:
                f_n = sp.sympify(f_n_raw(x))
        else:
            f_n = sp.sympify(f_n_raw, locals=local_dict)

        f_raw = get_attr('f')
        if callable(f_raw):
            try:
                f = sp.sympify(f_raw(x))
            except Exception:
                f = sp.sympify(f_raw(n, x))
        else:
            f = sp.sympify(f_raw, locals=local_dict)
            
        epsilon = sp.sympify(get_attr('epsilon'), locals=local_dict)
    except Exception:
        return [False] * 5

    # H_1: (X, Sigma, mu) is a measure space (domain is a valid interval)
    try:
        h1 = bool(a < b)
    except Exception:
        h1 = False

    # H_2: E is a measurable set with finite measure
    try:
        h2 = bool(b - a < sp.oo)
    except Exception:
        h2 = False

    # H_3: (f_n) is a sequence of measurable real-valued functions on E
    try:
        h3 = True
        for pt in [a + (b - a) * 0.3, a + (b - a) * 0.7]:
            for n_val in [1, 5, 10]:
                val = f_n.subs({x: pt, n: n_val})
                try:
                    val_f = float(val)
                    if math.isinf(val_f) or math.isnan(val_f):
                        h3 = False
                        break
                except Exception:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # H_4: (f_n) converges pointwise to f almost everywhere on E
    try:
        h4 = True
        for pt in [a + (b - a) * 0.3, a + (b - a) * 0.7]:
            lim = sp.limit(f_n.subs(x, pt), n, sp.oo)
            f_val = f.subs(x, pt)
            if lim != f_val:
                h4 = False
                break
    except Exception:
        h4 = False

    # ¬Q: Uniform convergence fails on all A with mu(E \ A) < epsilon
    # This occurs when the limit function f is infinite, making the standard 
    # uniform convergence metric in R undefined/fail.
    try:
        neg_q = False
        f_val1 = f.subs(x, a + (b - a) * 0.3)
        f_val2 = f.subs(x, a + (b - a) * 0.7)
        if f_val1 == sp.oo or f_val1 == -sp.oo or f_val2 == sp.oo or f_val2 == -sp.oo:
            if epsilon > 0 and epsilon < b - a:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: (X, Sigma, mu) is a measure space",
    "H_2: E is a measurable set with finite measure",
    "H_3: (f_n) is a sequence of measurable real-valued functions on E",
    "H_4: (f_n) converges pointwise to f almost everywhere on E",
    "¬Q: Uniform convergence fails on all A with mu(E \\ A) < epsilon"
]

N_HYP = 4
NEG_Q_INDEX = 4