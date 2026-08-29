import sympy
from sympy import Symbol
import math

# Top-level setup
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def get_coeffs(expr):
    try:
        expr = sympy.sympify(expr)
        if hasattr(expr, 'as_expr'):
            expr = expr.as_expr()
        expr = sympy.expand(expr)
        
        free_syms = expr.free_symbols
        if len(free_syms) > 1:
            return None
        elif len(free_syms) == 1:
            sym = list(free_syms)[0]
        else:
            sym = x
            
        coeffs_dict = expr.as_coefficients_dict()
        deg_coeff = {}
        for term, coeff in coeffs_dict.items():
            if term == 1:
                deg = 0
            elif term == sym:
                deg = 1
            elif isinstance(term, sympy.Pow) and term.base == sym:
                deg = int(term.exp)
            else:
                return None
            deg_coeff[deg] = int(coeff)
        
        if not deg_coeff:
            return 0, [0]
        
        min_deg = min(deg_coeff.keys())
        max_deg = max(deg_coeff.keys())
        coeffs = [deg_coeff.get(d, 0) for d in range(min_deg, max_deg + 1)]
        return min_deg, coeffs
    except Exception:
        return None

def conditions(witness):
    n = None
    f_k = 0
    f_coeffs = None

    # Parse witness
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            f_coeffs = witness.get('f_coeffs')
            f_k = witness.get('f_k', 0)
        elif isinstance(witness, tuple):
            if len(witness) >= 2:
                n = witness[0]
                if isinstance(witness[1], (list, tuple)):
                    f_coeffs = witness[1]
                    f_k = 0
                elif isinstance(witness[1], int) and len(witness) >= 3 and isinstance(witness[2], (list, tuple)):
                    f_k = witness[1]
                    f_coeffs = witness[2]
                else:
                    f_expr = witness[1]
                    res = get_coeffs(f_expr)
                    if res is not None:
                        f_k, f_coeffs = res
    except Exception:
        pass

    # H_1: R is a commutative ring with identity (we use Z/nZ)
    try:
        if n is not None:
            n = int(n)
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False

    # H_2: f(x) in R((x)) with a_k != 0
    try:
        h2 = False
        if h1 and isinstance(f_coeffs, (list, tuple)) and len(f_coeffs) > 0:
            try:
                f_coeffs = [int(c) for c in f_coeffs]
                valid_coeffs = True
            except Exception:
                valid_coeffs = False
                
            if valid_coeffs:
                first_nonzero_idx = -1
                for i, c in enumerate(f_coeffs):
                    if c % n != 0:
                        first_nonzero_idx = i
                        break
                if first_nonzero_idx != -1:
                    f_k = f_k + first_nonzero_idx
                    f_coeffs = f_coeffs[first_nonzero_idx:]
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: f(x) is a unit in R((x)) but a_k is not a unit in R
    try:
        neg_q = False
        if h1 and h2:
            a_k = f_coeffs[0]
            a_k_is_unit = math.gcd(a_k % n, n) == 1
            
            # Find prime factors of n
            primes = set()
            temp = n
            d = 2
            while d * d <= temp:
                if temp % d == 0:
                    primes.add(d)
                    while temp % d == 0:
                        temp //= d
                d += 1
            if temp > 1:
                primes.add(temp)
                
            # f(x) is a unit in (Z/nZ)((x)) iff for every prime factor p of n,
            # f(x) is not the zero series mod p.
            f_is_unit = True
            for p in primes:
                if all(c % p == 0 for c in f_coeffs):
                    f_is_unit = False
                    break
            
            neg_q = f_is_unit and not a_k_is_unit
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f(x) in R((x)) with a_k != 0",
    "¬Q: f(x) is a unit in R((x)) but a_k is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2