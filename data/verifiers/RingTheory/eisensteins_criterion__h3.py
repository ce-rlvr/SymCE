import sympy
from sympy import Poly
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: a_n is not an element of P",
    "H_4: a_i is an element of P for all 0 <= i < n",
    "H_5: a_0 is not an element of the ideal P^2",
    "¬Q: f(x) can be expressed as the product of two polynomials over R of strictly positive degree"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get("f")
            p = witness.get("p")
            n = witness.get("n", None)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                f, p = witness
                n = None
            elif len(witness) == 3:
                f, p, n = witness
            else:
                return [False] * 6
        else:
            return [False] * 6
            
        if f is None or p is None:
            return [False] * 6
            
        f = sympy.sympify(f)
        p = int(p)
        
        symbols = f.free_symbols
        if len(symbols) == 1:
            var = list(symbols)[0]
        elif len(symbols) == 0:
            var = x
        else:
            return [False] * 6
            
        f_poly = Poly(f, var, domain="ZZ")
        
        if n is None:
            n = f_poly.degree()
        else:
            n = int(n)
            
        h1 = f_poly.domain.is_IntegralDomain
        h2 = sympy.isprime(p)
        
        a_n = f_poly.nth(n)
        h3 = (a_n % p) != 0
        
        h4 = all((f_poly.nth(i) % p) == 0 for i in range(n))
        
        a_0 = f_poly.nth(0)
        h5 = (a_0 % (p**2)) != 0
        
        factors = f_poly.factor_list()
        pos_deg_factors = sum(mult for fac, mult in factors[1] if fac.degree() > 0)
        neg_q = pos_deg_factors >= 2
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]
        
    except Exception:
        return [False] * 6