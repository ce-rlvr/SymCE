import sympy
from sympy import symbols, Poly, S
import itertools

# Top-level setup
x, y, z, w = symbols('x y z w')
x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

def is_valid_poly(expr, vars):
    if expr == 0 or expr == S.Zero:
        return True
    try:
        p = Poly(expr, *vars)
        return all(c.is_integer for c in p.coeffs())
    except Exception:
        return False

def get_total_degree(expr, vars):
    if expr == 0 or expr == S.Zero:
        return float('-inf')
    try:
        if not vars:
            if expr == 0 or expr == S.Zero:
                return float('-inf')
            return 0
        p = Poly(expr, *vars)
        if p.is_zero:
            return float('-inf')
        return p.total_degree()
    except Exception:
        return float('inf')

def get_vars(polys, n):
    symbols_set = set()
    for poly in polys:
        if hasattr(poly, 'free_symbols'):
            symbols_set.update(poly.free_symbols)
    vars = list(symbols_set)
    if len(vars) > n:
        return None
    dummy_idx = 1
    while len(vars) < n:
        dummy = sympy.Symbol(f'd_{dummy_idx}')
        if dummy not in vars:
            vars.append(dummy)
        dummy_idx += 1
    return vars

def count_zeros(polys, vars, p):
    zeros = 0
    for pt in itertools.product(range(p), repeat=len(vars)):
        subs_dict = dict(zip(vars, pt))
        is_zero = True
        for poly in polys:
            if hasattr(poly, 'subs'):
                val = poly.subs(subs_dict)
            else:
                val = poly
            try:
                val = int(val)
            except Exception:
                is_zero = False
                break
            if val % p != 0:
                is_zero = False
                break
        if is_zero:
            zeros += 1
    return zeros

def conditions(witness):
    """
    witness should be a dictionary with keys: 'p', 'q', 'n', 'polys'
    or a tuple/list: (p, q, n, polys)
    """
    try:
        if isinstance(witness, dict):
            p_val = witness.get('p')
            q_val = witness.get('q')
            n = witness.get('n')
            polys = witness.get('polys')
        else:
            p_val, q_val, n, polys = witness
    except Exception:
        return [False, False, False, False]

    # H1: F_q is a finite field of characteristic p
    try:
        h1 = False
        if isinstance(p_val, int) and isinstance(q_val, int) and sympy.isprime(p_val):
            temp = q_val
            while temp % p_val == 0 and temp > 1:
                temp //= p_val
            if temp == 1 and q_val >= p_val:
                h1 = True
    except Exception:
        h1 = False

    # H2: f_1, ..., f_k are polynomials in F_q variables
    try:
        h2 = False
        vars = None
        if isinstance(polys, list) and isinstance(n, int) and n >= 0:
            vars = get_vars(polys, n)
            if vars is not None:
                h2 = all(is_valid_poly(poly, vars) for poly in polys)
    except Exception:
        h2 = False

    # H3: The sum of the total degrees is strictly less than n
    try:
        h3 = False
        if h2 and vars is not None:
            total_deg = 0.0
            for poly in polys:
                deg = get_total_degree(poly, vars)
                total_deg += deg
            if total_deg < n:
                h3 = True
    except Exception:
        h3 = False

    # Conclusion: N is divisible by p
    try:
        neg_q = False
        # For simplicity and robustness, we evaluate the counterexample over F_p
        # A valid counterexample exists for q = p.
        if h2 and vars is not None and q_val == p_val:
            zeros = count_zeros(polys, vars, p_val)
            if zeros % p_val != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p",
    "H_2: f_1 to f_k are polynomials in n variables over F_q",
    "H_3: The sum of the total degrees is strictly less than n",
    "not Q: N is not divisible by p"
]

N_HYP = 3
NEG_Q_INDEX = 3