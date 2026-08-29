import sympy
from sympy import Poly, symbols
import itertools
from sympy.ntheory import isprime

# Top-level setup for potential witness expressions
x, y, z, t, u, v, w = symbols('x y z t u v w')
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1:11')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (q, p, n, polys)
    where:
      - q: size of the finite field (we require q to be prime for simplicity)
      - p: the modulo integer for the conclusion
      - n: number of variables in the polynomial ring
      - polys: list of sympy expressions representing f_1, ..., f_r
    """
    try:
        q, p, n, polys = witness
    except Exception:
        return [False, False, False]

    # H_1: f_1, ..., f_r are polynomials in F_q variables
    h1 = False
    try:
        if isprime(q) and isinstance(p, int) and p >= 2 and isinstance(n, int) and n >= 1:
            if isinstance(polys, (list, tuple)) and len(polys) >= 1:
                symbols_set = set()
                for f in polys:
                    symbols_set.update(f.free_symbols)
                syms = list(symbols_set)
                
                if len(syms) <= n:
                    all_poly = True
                    for f in polys:
                        p_obj = Poly(f, *syms) if syms else Poly(f)
                        if not p_obj.domain.is_Integer:
                            all_poly = False
                            break
                    h1 = all_poly
    except Exception:
        h1 = False

    # H_2: sum_{i=1}^r deg(f_i) < n
    h2 = False
    try:
        if h1:
            total_deg = 0
            for f in polys:
                p_obj = Poly(f, *syms) if syms else Poly(f)
                deg = p_obj.total_degree()
                if deg == sympy.S.NegativeInfinity:
                    deg = 0
                else:
                    deg = int(deg)
                    if deg < 0:
                        deg = 0
                total_deg += deg
            h2 = total_deg < n
    except Exception:
        h2 = False

    # ¬Q: The number of common zeros of f_1, ..., f_r is not congruent to 0 modulo p
    neg_q_ok = False
    try:
        if h1:
            zeros_count = 0
            if not syms:
                all_zero = True
                for f in polys:
                    if int(f) % q != 0:
                        all_zero = False
                        break
                if all_zero:
                    zeros_count = q ** n
            else:
                if len(syms) > 12:
                    # Prevent timeout for unreasonably large number of variables
                    return [h1, h2, False]
                
                for pt in itertools.product(range(q), repeat=len(syms)):
                    sub_dict = dict(zip(syms, pt))
                    is_zero = True
                    for f in polys:
                        val = f.subs(sub_dict)
                        if int(val) % q != 0:
                            is_zero = False
                            break
                    if is_zero:
                        zeros_count += 1
                
                # Multiply by the number of choices for the variables that don't appear in the polynomials
                zeros_count *= q ** (n - len(syms))
            
            neg_q_ok = (zeros_count % p) != 0
    except Exception:
        neg_q_ok = False

    return [h1, h2, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_1 to f_r are polynomials in n variables over F_q",
    "H_2: sum of degrees of f_i is less than n",
    "¬Q: The number of common zeros is not congruent to 0 modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2