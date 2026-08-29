import sympy
from sympy import symbols, expand, Poly
from sympy.ntheory import factorint
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_irreducible
import itertools

# Top-level setup
x, y, z, w = symbols('x y z w')
x0, x1, x2, x3, x4, x5 = symbols('x0 x1 x2 x3 x4 x5')
_alpha_gf = symbols('_alpha_gf')

def conditions(witness):
    """
    witness is expected to be a tuple: (q, vars_list, polys)
    where:
      - q is the order of the finite field (an integer prime power)
      - vars_list is a list of sympy symbols representing the n variables
      - polys is a list of sympy expressions representing the polynomials P_1, ..., P_k
    """
    try:
        q, vars_list, polys = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a finite field of order q
    try:
        if not isinstance(q, int) or q <= 1:
            h1 = False
        else:
            factors = factorint(q)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False
        
    # H2: P_1, ..., P_k are polynomials in n variables over F
    try:
        h2 = True
        if not isinstance(vars_list, (list, tuple)) or not isinstance(polys, (list, tuple)):
            h2 = False
        elif len(polys) == 0:
            h2 = False
        else:
            for P in polys:
                poly = Poly(P, *vars_list)
                for c in poly.coeffs():
                    if not isinstance(c, (int, sympy.Integer)):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # H3: The sum of the total degrees of the polynomials P_1, ..., P_k is strictly less than n
    try:
        n = len(vars_list)
        total_deg_sum = 0
        for P in polys:
            poly = Poly(P, *vars_list)
            if poly.is_zero:
                deg = 0
            else:
                deg = max(sum(monom) for monom in poly.monoms())
            total_deg_sum += deg
        h3 = total_deg_sum < n
    except Exception:
        h3 = False
        
    # neg_Q: The system of equations has strictly less than q distinct solutions in F^n
    try:
        factors = factorint(q)
        p, m = list(factors.items())[0]
        
        if m == 1:
            count = 0
            for vals in itertools.product(range(p), repeat=len(vars_list)):
                val_dict = dict(zip(vars_list, vals))
                ok = True
                for P in polys:
                    if int(expand(P.subs(val_dict))) % p != 0:
                        ok = False
                        break
                if ok:
                    count += 1
            neg_q = count < q
        else:
            irred_coeffs = gf_irreducible(m, p, ZZ)
            irred_poly = sum(int(c) * _alpha_gf**(len(irred_coeffs)-1-i) for i, c in enumerate(irred_coeffs))
            
            elements = []
            for coeffs in itertools.product(range(p), repeat=m):
                elements.append(sum(c * _alpha_gf**i for i, c in enumerate(coeffs)))
                
            count = 0
            for vals in itertools.product(elements, repeat=len(vars_list)):
                val_dict = dict(zip(vars_list, vals))
                ok = True
                for P in polys:
                    res = expand(P.subs(val_dict))
                    res_poly = Poly(res, _alpha_gf, domain=f'GF({p})')
                    _, rem = res_poly.div(Poly(irred_poly, _alpha_gf, domain=f'GF({p})'))
                    if not rem.is_zero:
                        ok = False
                        break
                if ok:
                    count += 1
            neg_q = count < q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: P_1, ..., P_k are polynomials in n variables over F",
    "H_3: The sum of the total degrees of the polynomials P_1, ..., P_k is strictly less than n",
    "¬Q: The system of equations has strictly less than q distinct solutions in F^n"
]

N_HYP = 3
NEG_Q_INDEX = 3