import sympy
from sympy import Poly, Mul, expand, roots
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness elements
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
            F = witness.get('F')
            S = witness.get('S')
            g = witness.get('g')
            E_1 = witness.get('E_1')
            E_2 = witness.get('E_2')
        else:
            F, S, g, E_1, E_2 = witness
    except Exception:
        return [False] * 4 + [False]

    # H1: F is a field
    try:
        h1 = hasattr(F, 'is_Field') and F.is_Field
        if not h1:
            h1 = isinstance(F, sympy.polys.domains.Field)
    except Exception:
        h1 = False

    # H2: S is a finite set of polynomials over F
    try:
        h2 = isinstance(S, (list, set, tuple)) and len(S) > 0
        if h2:
            for p in S:
                expr_p = p.as_expr() if hasattr(p, 'as_expr') else p
                poly_p = Poly(expr_p, x, domain=F)
    except Exception:
        h2 = False

    # H3: g is the product of the polynomials in S
    try:
        expr_S = [p.as_expr() if hasattr(p, 'as_expr') else p for p in S]
        expr_g = g.as_expr() if hasattr(g, 'as_expr') else g
        h3 = expand(Mul(*expr_S)) == expand(expr_g)
    except Exception:
        h3 = False

    # H4: E_2 is a splitting field of g over F
    try:
        expr_g = g.as_expr() if hasattr(g, 'as_expr') else g
        from sympy import factor_list
        factors = factor_list(expr_g, domain=E_2)[1]
        splits = all(Poly(f, x, domain=E_2).degree() == 1 for f, _ in factors)
        
        if not splits:
            h4 = False
        else:
            if F == E_2:
                h4 = True
            elif hasattr(E_2, 'ext'):
                h4 = True
            else:
                h4 = False
    except Exception:
        h4 = False

    # ¬Q: E_1 and E_2 are not isomorphic over F
    try:
        def are_isomorphic(E1, E2):
            if E1 == E2:
                return True
            deg1 = E1.ext.degree() if hasattr(E1, 'ext') else 1
            deg2 = E2.ext.degree() if hasattr(E2, 'ext') else 1
            if deg1 != deg2:
                return False
            if deg1 == 1:
                return True
            from sympy import factor_list
            factors = factor_list(E1.mod, domain=E2)[1]
            return any(f.degree() == 1 for f, _ in factors)
        
        neg_q = not are_isomorphic(E_1, E_2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: S is a finite set of polynomials over F",
    "H_3: g is the product of the polynomials in S",
    "H_4: E_2 is a splitting field of g over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 4
NEG_Q_INDEX = 4