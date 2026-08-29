import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.polys

# Top-level setup
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

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: K is an extension field of F",
    "H_3: alpha in K is algebraic over F",
    "H_4: m(x) is the minimal polynomial of alpha over F",
    "¬Q: m(x) has a root with multiplicity > 1"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K = witness.get('K')
            alpha = witness.get('alpha')
            m = witness.get('m')
            x = witness.get('x')
        else:
            F, K, alpha, m, x = witness
    except Exception:
        return [False, False, False, False, False]

    h1 = False
    try:
        if getattr(F, 'is_Field', False):
            char = getattr(F, 'char', None)
            if char == 0:
                h1 = True
            elif getattr(F, 'is_FiniteField', False):
                h1 = True
            elif type(F).__name__ == 'FractionField':
                h1 = False
            else:
                h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if getattr(K, 'is_Field', False) and getattr(F, 'is_Field', False):
            if K == F:
                h2 = True
            else:
                try:
                    if K.unify(F) == K:
                        h2 = True
                except Exception:
                    pass
                if not h2:
                    if getattr(K, 'domain', None) == F:
                        h2 = True
                    elif getattr(K, 'dom', None) == F:
                        h2 = True
    except Exception:
        pass

    h3 = False
    try:
        val = K.from_sympy(sympy.sympify(alpha))
        if val is not None:
            h3 = True
    except Exception:
        pass

    h4 = False
    try:
        m_expr = sympy.sympify(m)
        x_sym = sympy.sympify(x)
        poly_m = sympy.Poly(m_expr, x_sym, domain=F)
        
        if poly_m.LC() == 1:
            val_expr = sympy.simplify(m_expr.subs(x_sym, alpha))
            val_K = K.from_sympy(sympy.sympify(val_expr))
            if val_K == K.zero:
                if poly_m.is_irreducible:
                    h4 = True
    except Exception:
        pass

    neg_q = False
    try:
        m_expr = sympy.sympify(m)
        x_sym = sympy.sympify(x)
        poly_m = sympy.Poly(m_expr, x_sym, domain=F)
        poly_diff = poly_m.diff()
        
        gcd_poly = poly_m.gcd(poly_diff)
        if gcd_poly.degree() > 0:
            neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]