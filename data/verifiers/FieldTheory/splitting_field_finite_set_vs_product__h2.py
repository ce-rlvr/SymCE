import sympy
import sympy.combinatorics
import sympy.matrices
from sympy import Symbol, expand, roots, Poly
from sympy.polys.numberfields import primitive_element, field_isomorphism

# Top-level setup for witness expressions
x = Symbol('x')

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_field(F):
    return F in ['QQ', sympy.QQ, 'Q', sympy.S.Rationals]

def is_splitting_field(E_poly, polys, x_sym):
    try:
        E_poly_obj = Poly(E_poly, x_sym, domain='QQ')
        if not E_poly_obj.is_irreducible:
            return False
            
        all_roots = []
        for p in polys:
            p_poly = Poly(p, x_sym, domain='QQ')
            rts = roots(p_poly.as_expr(), x_sym)
            if sum(rts.values()) != p_poly.degree():
                return False
            for r in rts.keys():
                if r not in all_roots:
                    all_roots.append(r)
                    
        if not all_roots:
            return E_poly_obj.degree() == 1
            
        res = primitive_element(all_roots, x_sym)
        minpoly = res[0] if isinstance(res, tuple) else res
        minpoly_expr = Poly(minpoly, x_sym, domain='QQ').monic().as_expr()
        
        E_poly_expr = E_poly_obj.monic().as_expr()
        iso = field_isomorphism(E_poly_expr, minpoly_expr)
        return iso is not None
    except Exception:
        return False

def conditions(witness):
    if not isinstance(witness, dict):
        return [False, False, False, False, False]

    F = witness.get("F")
    S = witness.get("S", [])
    f_list = witness.get("f_list", [])
    g = witness.get("g")
    E1 = witness.get("E1")
    E2 = witness.get("E2")
    
    # H1: F is a field
    try:
        h1 = is_field(F)
    except Exception:
        h1 = False
        
    # H2: g(x) = f_1(x)...f_k(x)
    try:
        if not f_list:
            h2 = False
        else:
            prod = 1
            for f in f_list:
                prod *= f
            h2 = bool(expand(g) == expand(prod))
    except Exception:
        h2 = False
        
    # H3: E1 is a splitting field of S over F
    try:
        if not isinstance(S, list):
            h3 = False
        else:
            h3 = is_splitting_field(E1, S, x)
    except Exception:
        h3 = False
        
    # H4: E2 is a splitting field of g over F
    try:
        h4 = is_splitting_field(E2, [g], x)
    except Exception:
        h4 = False
        
    # ¬Q: E1 and E2 are NOT isomorphic over F
    try:
        E1_monic = Poly(E1, x, domain='QQ').monic().as_expr()
        E2_monic = Poly(E2, x, domain='QQ').monic().as_expr()
        iso = field_isomorphism(E1_monic, E2_monic)
        neg_q = (iso is None)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: g(x) = f_1(x)f_2(x)...f_k(x)",
    "H_3: E_1 is a splitting field of the set S over F",
    "H_4: E_2 is a splitting field of the polynomial g(x) over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 4
NEG_Q_INDEX = 4