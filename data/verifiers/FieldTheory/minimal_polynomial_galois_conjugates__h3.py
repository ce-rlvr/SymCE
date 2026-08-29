import sympy
from sympy import Poly, factor, minpoly
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

def conditions(witness):
    """
    witness is expected to be a tuple: (alpha, E_prim_elem, m_poly)
    where:
      - alpha is an algebraic number
      - E_prim_elem is an algebraic number generating the extension E over QQ
      - m_poly is a SymPy expression representing m(x) in QQ[x]
    """
    try:
        alpha, E_prim_elem, m_poly = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    # We fix F = QQ, which is a field.
    h1_ok = True
    
    # H_2: E is a finite Galois extension of F
    try:
        p_E = minpoly(E_prim_elem, x)
        factored = factor(p_E, extension=E_prim_elem)
        if factored.is_Mul:
            factors = factored.args
        else:
            factors = [factored]
            
        h2_ok = True
        for f in factors:
            if f.has(x):
                if Poly(f, x).degree() != 1:
                    h2_ok = False
                    break
    except Exception:
        h2_ok = False
        
    # H_3: m(x) in F[x] is the minimal polynomial of alpha over F
    try:
        expected_m = minpoly(alpha, x)
        p1 = Poly(m_poly, x, domain='QQ')
        p2 = Poly(expected_m, x, domain='QQ')
        h3_ok = (p1 == p2)
    except Exception:
        h3_ok = False
        
    # ¬Q: The conclusion fails
    try:
        deg_E = minpoly(E_prim_elem, x).degree()
        elem, poly = primitive_element([alpha, E_prim_elem], x=x)
        deg_both = poly.degree()
        
        if deg_both > deg_E:
            # alpha is not in E, so the action of Gal(E/F) on alpha is undefined.
            # Thus the set S is undefined, and the equality fails.
            q_holds = False
        else:
            # alpha is in E. The orbit of alpha under Gal(E/F) is exactly the set of roots
            # of its minimal polynomial over F. Thus the product is exactly minpoly(alpha, x).
            expected_m = minpoly(alpha, x)
            try:
                p1 = Poly(m_poly, x, domain='QQ')
                p2 = Poly(expected_m, x, domain='QQ')
                q_holds = (p1 == p2)
            except Exception:
                q_holds = False
                
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a finite Galois extension of F",
    "H_3: m is the minimal polynomial of alpha over F",
    "¬Q: m is not the product of x - beta for beta in the orbit"
]

N_HYP = 3
NEG_Q_INDEX = 3