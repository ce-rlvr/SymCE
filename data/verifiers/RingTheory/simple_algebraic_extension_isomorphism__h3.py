import sympy
import sympy.combinatorics
import sympy.matrices
from sympy.abc import x

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            F, E, alpha, m = witness
        elif len(witness) == 2:
            alpha, m = witness
            F = sympy.QQ
            try:
                if alpha in sympy.QQ:
                    E = sympy.QQ
                else:
                    E = sympy.QQ.algebraic_field(alpha)
            except Exception:
                E = sympy.QQ
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if isinstance(F, str) and isinstance(E, str):
            h1 = True
        else:
            h1 = getattr(F, 'is_Field', False) and getattr(E, 'is_Field', False)
            if not h1:
                if F in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
                    h1 = True
    except Exception:
        h1 = False

    try:
        if isinstance(E, str):
            in_E = True
        elif E in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            in_E = True
        else:
            in_E = alpha in E
    except Exception:
        in_E = False

    try:
        mp = sympy.minpoly(alpha, x)
        is_alg = True
    except Exception:
        is_alg = False

    h2 = in_E and is_alg

    try:
        if isinstance(m, sympy.Poly):
            m_poly = m
            m_var = m.gen
        else:
            free = getattr(m, "free_symbols", set())
            m_var = list(free)[0] if free else x
            if hasattr(F, 'is_Field') and F.is_Field:
                m_poly = sympy.Poly(m, m_var, domain=F)
            else:
                m_poly = sympy.Poly(m, m_var)
                
        is_irred = m_poly.is_irreducible
        
        if not is_irred:
            neg_q = True
        else:
            mp = sympy.minpoly(alpha, m_var)
            deg_alpha = sympy.Poly(mp, m_var).degree()
            if m_poly.degree() != deg_alpha:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E is an extension field of F",
    "H_2: alpha in E is algebraic over F",
    "¬Q: quotient ring is not isomorphic to simple extension"
]

N_HYP = 2
NEG_Q_INDEX = 2