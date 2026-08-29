import sympy
from sympy import Poly, isprime, eye, zeros
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            f = witness['f']
        else:
            p = witness[0]
            f = witness[1]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    try:
        if hasattr(f, 'free_symbols'):
            symbols = f.free_symbols
            if len(symbols) == 1:
                var = list(symbols)[0]
            else:
                var = sympy.Symbol('x')
        else:
            var = sympy.Symbol('x')
            
        f_poly = sympy.Poly(f, var)
        h2 = bool(f_poly.degree() >= 1)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            f_poly_gf = sympy.Poly(f, var, domain=f'GF({p})')
            factors = f_poly_gf.factor_list()
            
            sqf = sympy.Poly(1, var, domain=f'GF({p})')
            for fac, mult in factors[1]:
                sqf = sqf * fac
            sqf = sqf.monic()
            
            if sqf.degree() <= 0:
                is_vs = False
            else:
                coeffs = sqf.all_coeffs()
                deg = sqf.degree()
                
                if coeffs[-1] != 0:
                    is_vs = False
                else:
                    is_vs = True
                    for i, c in enumerate(coeffs):
                        if c != 0:
                            power = deg - i
                            if power == 0:
                                continue
                            
                            temp = power
                            while temp % p == 0:
                                temp //= p
                            if temp != 1:
                                is_vs = False
                                break
            neg_q = not is_vs
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic p > 0",
    "H_2: L is the splitting field of f(x) over K",
    "¬Q: The roots of f(x) do not form a vector space over F_p, or the Galois action is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2