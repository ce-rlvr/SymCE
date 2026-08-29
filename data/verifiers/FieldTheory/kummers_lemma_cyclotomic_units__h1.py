import sympy
from sympy import Symbol, Poly, cyclotomic_poly, resultant

x = Symbol('x')

def conditions(witness):
    try:
        p, u_obj = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(p, int) and p >= 1
    except Exception:
        h1 = False
        
    try:
        if isinstance(u_obj, (list, tuple)):
            U_expr = sum(c * x**i for i, c in enumerate(u_obj))
        else:
            U_expr = sympy.sympify(u_obj, locals={'x': x})
            
        Phi = cyclotomic_poly(p, x)
        Phi_poly = Poly(Phi, x, domain='ZZ')
        U_poly = Poly(U_expr, x, domain='ZZ').rem(Phi_poly)
        
        res = resultant(U_poly.as_expr(), Phi, x)
        h2 = (abs(res) == 1)
    except Exception:
        h2 = False
        
    try:
        if isinstance(u_obj, (list, tuple)):
            U_expr = sum(c * x**i for i, c in enumerate(u_obj))
        else:
            U_expr = sympy.sympify(u_obj, locals={'x': x})
            
        Phi = cyclotomic_poly(p, x)
        Phi_poly = Poly(Phi, x, domain='ZZ')
        U_poly = Poly(U_expr, x, domain='ZZ').rem(Phi_poly)
        
        U_inv_poly = Poly(0, x, domain='ZZ')
        x_inv = Poly(x**(p-1), x, domain='ZZ').rem(Phi_poly)
        
        for c in U_poly.all_coeffs():
            U_inv_poly = (U_inv_poly * x_inv + Poly(c, x, domain='ZZ')).rem(Phi_poly)
            
        conclusion_holds = False
        x_poly = Poly(x, x, domain='ZZ')
        x_2k = Poly(1, x, domain='ZZ')
        x_2 = (x_poly * x_poly).rem(Phi_poly)
        
        for k in range(p):
            test_poly = (U_inv_poly * x_2k).rem(Phi_poly)
            if U_poly == test_poly:
                conclusion_holds = True
                break
            x_2k = (x_2k * x_2).rem(Phi_poly)
                
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_p is a primitive p-th root of unity",
    "H_2: u is a unit in the ring of integers of the p-th cyclotomic field",
    "¬Q: u cannot be written as zeta_p^k * v for any integer k and real unit v"
]

N_HYP = 2
NEG_Q_INDEX = 2