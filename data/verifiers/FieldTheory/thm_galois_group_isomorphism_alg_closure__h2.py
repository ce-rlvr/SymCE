import sympy
from sympy import Poly, QQ, factor_list, RootOf
from sympy.abc import x

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Witness is expected to be a tuple of two polynomials (P_K, P_E) in x over QQ.
    P_K is the minimal polynomial of a primitive element of K over F.
    P_E is the minimal polynomial of a primitive element of E over F.
    F is implicitly the field of rational numbers QQ.
    """
    try:
        P_K_expr, P_E_expr = witness
        P_K = Poly(P_K_expr, x, domain=QQ)
        P_E = Poly(P_E_expr, x, domain=QQ)
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    # F is QQ, which is always a field.
    h1 = True
    
    # Check irreducibility to ensure they define valid field extensions over QQ
    try:
        if not P_K.is_irreducible or not P_E.is_irreducible:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_2: K is a subfield of E containing F
    try:
        beta = RootOf(P_E, 0)
        factors_K = factor_list(P_K, extension=beta)[1]
        linear_factors_K = [f[0] for f in factors_K if f[0].degree() == 1]
        h2 = len(linear_factors_K) > 0
    except Exception:
        h2 = False
        
    # H_3: K is a finite Galois extension of F
    try:
        alpha = RootOf(P_K, 0)
        factors_K_self = factor_list(P_K, extension=alpha)[1]
        h3 = all(f[0].degree() == 1 for f in factors_K_self)
    except Exception:
        h3 = False
        
    # ¬Q: The Galois group Gal(K/F) is NOT isomorphic to the quotient group Aut(E/F) / Aut(E/K)
    try:
        if not (h2 and h3):
            neg_q = False
        else:
            gal_K_F_size = P_K.degree()
            
            factors_E = factor_list(P_E, extension=beta)[1]
            linear_factors_E = [f[0] for f in factors_E if f[0].degree() == 1]
            
            def get_expr_poly(f):
                c0 = f.coeffs()[-1]
                coeffs = None
                if hasattr(c0, 'rep') and hasattr(c0.rep, 'to_list'):
                    coeffs = c0.rep.to_list()
                elif hasattr(c0, 'to_list'):
                    coeffs = c0.to_list()
                
                if coeffs is not None:
                    return Poly([-sympy.sympify(c) for c in coeffs], x, domain=QQ)
                    
                if hasattr(c0, 'as_expr'):
                    expr = c0.as_expr()
                elif hasattr(c0, 'to_expr'):
                    expr = c0.to_expr()
                else:
                    expr = sympy.sympify(c0)
                    
                expr_x = expr.subs(beta, x)
                return Poly(-expr_x, x, domain=QQ)
                
            g_poly = get_expr_poly(linear_factors_K[0])
            
            aut_E_F = []
            for f in linear_factors_E:
                aut_E_F.append(get_expr_poly(f))
                
            aut_E_K = []
            for p in aut_E_F:
                comp = g_poly.compose(p)
                rem = comp % P_E
                if ((rem - g_poly) % P_E).is_zero:
                    aut_E_K.append(p)
                    
            if len(aut_E_K) == 0:
                neg_q = False
            else:
                id_poly = Poly(x, x, domain=QQ)
                inverses = {}
                for g in aut_E_F:
                    for h in aut_E_F:
                        if ((g.compose(h) % P_E) - id_poly).is_zero:
                            inverses[g] = h
                            break
                            
                is_normal = True
                for g in aut_E_F:
                    if g not in inverses:
                        is_normal = False
                        break
                    g_inv = inverses[g]
                    for n in aut_E_K:
                        step1 = g.compose(n) % P_E
                        conj = step1.compose(g_inv) % P_E
                        if not any(((conj - nk) % P_E).is_zero for nk in aut_E_K):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
                if not is_normal:
                    neg_q = True
                else:
                    quotient_size = len(aut_E_F) // len(aut_E_K)
                    if gal_K_F_size != quotient_size:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a subfield of E containing F",
    "H_3: K is a finite Galois extension of F",
    "¬Q: The Galois group Gal(K/F) is not isomorphic to the quotient group Aut(E/F) / Aut(E/K)"
]

N_HYP = 3
NEG_Q_INDEX = 3