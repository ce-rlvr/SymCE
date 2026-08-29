import sympy
from sympy import Poly, ZZ, QQ, Symbol

x = Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "The content of Phi(f) in S[x] is associate to phi(c) in S"
    where the hypothesis "c is the content of f" was dropped.
    """
    R = ZZ
    S = ZZ
    phi = lambda val: val
    Phi = lambda val: val
    
    if isinstance(witness, dict):
        R = witness.get('R', ZZ)
        S = witness.get('S', ZZ)
        phi = witness.get('phi', lambda val: val)
        Phi = witness.get('Phi', lambda val: val)
        f = witness.get('f', None)
        c = witness.get('c', None)
    elif isinstance(witness, tuple) and len(witness) == 2:
        f, c = witness
    else:
        f, c = None, None

    # H_1: R and S are Unique Factorization Domains
    try:
        h1 = bool(R.is_UFD and S.is_UFD)
    except Exception:
        h1 = False

    # H_2: phi: R -> S is a ring isomorphism
    try:
        h2 = (phi(R.one) == S.one) and (phi(R.zero) == S.zero)
    except Exception:
        h2 = False

    # H_3: Phi is the polynomial ring isomorphism induced by phi
    try:
        f_poly = Poly(f, x)
        Phi_f_poly = Poly(Phi(f), x)
        h3 = True
        if f_poly.is_zero and Phi_f_poly.is_zero:
            h3 = True
        elif f_poly.degree() != Phi_f_poly.degree():
            h3 = False
        else:
            for i in range(f_poly.degree() + 1):
                if phi(f_poly.nth(i)) != Phi_f_poly.nth(i):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # H_4: f is a non-zero polynomial
    try:
        f_poly = Poly(f, x)
        h4 = not f_poly.is_zero
        if h4:
            for c_f in f_poly.coeffs():
                try:
                    R.from_sympy(c_f)
                except Exception:
                    h4 = False
                    break
    except Exception:
        h4 = False

    # ¬Q: The content of Phi(f) is NOT associate to phi(c) in S
    try:
        Phi_f_poly = Poly(Phi(f), x)
        cont = Phi_f_poly.content()
        phi_c = phi(c)
        
        is_assoc = False
        if cont == 0 and phi_c == 0:
            is_assoc = True
        elif cont != 0 and phi_c != 0:
            try:
                c_S = S.from_sympy(cont)
                phic_S = S.from_sympy(phi_c)
                q1, r1 = S.div(c_S, phic_S)
                q2, r2 = S.div(phic_S, c_S)
                if r1 == 0 and r2 == 0 and S.is_unit(q1) and S.is_unit(q2):
                    is_assoc = True
            except Exception:
                try:
                    if sympy.simplify(abs(cont) - abs(phi_c)) == 0:
                        is_assoc = True
                except Exception:
                    pass
        
        neg_q = not is_assoc
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are Unique Factorization Domains",
    "H_2: phi is a ring isomorphism",
    "H_3: Phi is the polynomial ring isomorphism induced by phi",
    "H_4: f is a non-zero polynomial",
    "¬Q: The content of Phi(f) is not associate to phi(c) in S"
]

N_HYP = 4
NEG_Q_INDEX = 4