import math
import sympy

# Top-level setup
x, y, n = sympy.symbols('x y n')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness must provide:
      - 'a', 'b': endpoints of the interval
      - 'f_n': a callable or sympy expression f_n(n, x) representing the sequence of functions
      - 'f': a callable or sympy expression f(x) representing the limit function
    """
    try:
        a = float(witness['a'])
        b = float(witness['b'])
        f_n_obj = witness['f_n']
        f_obj = witness['f']
        
        if callable(f_n_obj):
            f_n = f_n_obj
        else:
            f_n_sym = sympy.lambdify((n, x), f_n_obj, modules=['math', 'sympy'])
            f_n = lambda n_val, x_val: float(f_n_sym(n_val, x_val))
            
        if callable(f_obj):
            f = f_obj
        else:
            f_sym = sympy.lambdify(x, f_obj, modules=['math', 'sympy'])
            f = lambda x_val: float(f_sym(x_val))
            
        # Test evaluation to ensure validity
        _ = f_n(1, a)
        _ = f(a)
    except Exception:
        return [False, False, False, False]

    # H1: The domain is a compact interval in R
    try:
        h1 = (a < b) and math.isfinite(a) and math.isfinite(b)
    except Exception:
        h1 = False

    # H2: The sequence of functions is monotonically non-decreasing
    try:
        h2 = True
        for n_val in [1, 2, 5, 10, 50]:
            xs = [a + i * (b - a) / 100 for i in range(101)]
            for i in range(100):
                if float(f_n(n_val, xs[i])) > float(f_n(n_val, xs[i+1])) + 1e-7:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: The limit function is continuous
    try:
        h3 = True
        xs = [a + i * (b - a) / 100 for i in range(101)]
        for x_val in xs:
            for dx in [-1e-7, 1e-7]:
                x_adj = x_val + dx
                if a <= x_adj <= b:
                    if abs(float(f(x_val)) - float(f(x_adj))) > 1e-2:
                        h3 = False
                        break
            if not h3:
                break
        
        # Also verify that f is indeed the limit function on the interior
        if h3:
            interior_xs = [a + i * (b - a) / 10 for i in range(1, 10)]
            for x_val in interior_xs:
                val_large = float(f_n(100000, x_val))
                if abs(val_large - float(f(x_val))) > 0.2:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # NegQ: The sequence does not converge uniformly
    try:
        def get_max_diff(n_val):
            xs = [a + i * (b - a) / 200 for i in range(201)]
            m = 0.0
            for x_val in xs:
                try:
                    d = abs(float(f_n(n_val, x_val)) - float(f(x_val)))
                    if d > m: 
                        m = d
                except Exception:
                    pass
            return m

        diff_100 = get_max_diff(100)
        diff_10000 = get_max_diff(10000)
        
        # If the maximum difference does not decay to 0, it's not uniformly convergent.
        if diff_10000 > 0.01 and diff_10000 >= diff_100 * 0.9:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The domain is a compact interval in R",
    "H_2: The sequence of functions is monotonically non-decreasing",
    "H_3: The limit function is continuous",
    "¬Q: The sequence does not converge uniformly"
]

N_HYP = 3
NEG_Q_INDEX = 3