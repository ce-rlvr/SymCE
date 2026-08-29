import sympy
from sympy import Poly, Symbol
from sympy.abc import x, y, z

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "H_2: f is a non-constant polynomial over F",
    "¬Q: The splitting field K is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                F, f = witness
                K_given = None
            elif len(witness) == 3:
                F, f, K_given = witness
            else:
                F = sympy.CC
                f = witness
                K_given = None
        else:
            F = sympy.CC
            f = witness
            K_given = None
    except Exception:
        return [False, False, False]

    # H1: F is an algebraically closed field
    try:
        if F == sympy.CC or str(F) in ['CC', 'Complexes']:
            h1 = True
        elif hasattr(F, 'is_algebraically_closed') and F.is_algebraically_closed:
            h1 = True
    except Exception:
        pass

    poly_f = None
    # H2: f is a non-constant polynomial over F
    try:
        poly_f = sympy.Poly(f)
        if poly_f.degree() >= 1 and len(poly_f.gens) == 1 and poly_f.gens[0].is_Symbol:
            h2 = True
    except Exception:
        pass

    # neg_Q: The splitting field K is not equal to F
    try:
        if K_given is not None:
            neg_q = (K_given != F)
        else:
            if h1:
                neg_q = False
            else:
                if F == sympy.QQ or str(F) == 'QQ':
                    rts = sympy.roots(f)
                    degree = poly_f.degree() if poly_f is not None else sympy.Poly(f).degree()
                    if sum(rts.values()) == degree and all(r.is_Rational for r in rts.keys()):
                        neg_q = False
                    else:
                        neg_q = True
                elif F == sympy.RR or str(F) == 'RR':
                    rts = sympy.roots(f)
                    degree = poly_f.degree() if poly_f is not None else sympy.Poly(f).degree()
                    if sum(rts.values()) == degree and all(r.is_real for r in rts.keys()):
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]