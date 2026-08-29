import sympy
from sympy import Poly, simplify, minpoly, roots, Rational, Integer, I, pi, E, sqrt, eye, zeros, primitive_element
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for named objects
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
    "H_1: F is a field",
    "H_2: E is the splitting field of f(x) over F",
    "H_3: Gal(E/F) is an abelian group",
    "H_4: alpha is a root of f(x)",
    "¬Q: F(alpha) is not equal to E"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    h4 = False
    neg_q = False
    
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False, False]
            
        f_expr, alpha = witness
        
        h1 = True
        h2 = True
        
        try:
            f_poly = Poly(f_expr, x, domain='QQ')
        except Exception:
            return [h1, h2, False, False, False]
            
        try:
            factors = f_poly.factor_list()[1]
            h3 = all(fac.degree() <= 2 for fac, _ in factors)
        except Exception:
            h3 = False
            
        try:
            val = simplify(f_expr.subs(x, alpha))
            h4 = bool(val == 0)
        except Exception:
            h4 = False
            
        if not h4:
            return [h1, h2, h3, h4, False]
            
        try:
            minpoly_alpha = minpoly(alpha, x)
            deg_F_alpha = minpoly_alpha.degree()
            
            generators = []
            for fac, _ in factors:
                if fac.degree() >= 2:
                    fac_roots = roots(fac, x)
                    if fac_roots:
                        if fac.degree() == 2:
                            generators.append(list(fac_roots.keys())[0])
                        else:
                            generators.extend(list(fac_roots.keys()))
                            
            unique_gens = list(set(generators))
            
            if len(unique_gens) == 0:
                deg_E = 1
            elif len(unique_gens) == 1:
                minpoly_E = minpoly(unique_gens[0], x)
                deg_E = minpoly_E.degree()
            else:
                minpoly_E, _ = primitive_element(unique_gens, x)
                deg_E = minpoly_E.degree()
                
            neg_q = bool(deg_F_alpha < deg_E)
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, h4, neg_q]