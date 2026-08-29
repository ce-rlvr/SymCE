import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from sympy.polys import Poly, factor_list
from sympy.abc import x, y, z, t, u, v, a, b, c

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

CONDITION_LABELS = [
    "H_1: E is an algebraic extension of F",
    "¬Q: E is not a separable extension of F, or F is not a perfect field"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        p = witness['p']
        poly_expr = witness['poly']
        x_var = witness['x']
        
        if isinstance(poly_expr, Poly):
            poly_expr = poly_expr.as_expr()
            
        if p != 0 and not isprime(p):
            return [False, False]
            
        p_x = Poly(poly_expr, x_var)
        deg_x = p_x.degree()
        if deg_x < 1:
            h1 = False
        else:
            if p > 0:
                coeff, factors = factor_list(poly_expr, modulus=p)
            else:
                coeff, factors = factor_list(poly_expr)
                
            x_factors = [(base, exp) for (base, exp) in factors if Poly(base, x_var).degree() >= 1]
            h1 = (len(x_factors) == 1 and x_factors[0][1] == 1 and Poly(x_factors[0][0], x_var).degree() == deg_x)
                
        if p == 0:
            E_is_separable = True
            F_is_perfect = True
        else:
            deriv = poly_expr.diff(x_var)
            free_syms = list(poly_expr.free_symbols)
            if x_var in free_syms:
                free_syms.remove(x_var)
            gens = [x_var] + free_syms
            
            deriv_poly = Poly(deriv, *gens)
            
            if deriv_poly.is_zero:
                E_is_separable = False
            else:
                E_is_separable = not all(int(c_val) % p == 0 for c_val in deriv_poly.coeffs())
                
            if len(free_syms) > 0:
                F_is_perfect = False
            else:
                F_is_perfect = True
                
        Q_holds = E_is_separable and F_is_perfect
        neg_q = not Q_holds
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]