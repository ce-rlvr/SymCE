import sympy
from sympy import Poly
from sympy.abc import x, y, z

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    Let R be a UFD, F its fraction field, f a primitive polynomial over R.
    Then f is irreducible over R iff f is irreducible over F.
    """
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            try:
                free_syms = list(witness.free_symbols)
            except Exception:
                free_syms = []
            if len(free_syms) == 1:
                f = Poly(witness, free_syms[0])
            else:
                f = Poly(witness, x)
    except Exception:
        return [False, False, False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        R = f.domain
        if R == sympy.ZZ or R == sympy.QQ:
            h1 = True
        else:
            h1 = getattr(R, 'is_UFD', False)
            if h1 is None:
                h1 = False
    except Exception:
        h1 = False

    # H_2: F is the field of fractions of R
    try:
        F = R.frac_field()
        if F == sympy.QQ or getattr(F, 'is_Field', False):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: f is a polynomial over R
    try:
        h3 = isinstance(f, Poly)
    except Exception:
        h3 = False

    # H_4: f is primitive over R
    try:
        c = f.content()
        if R == sympy.ZZ:
            h4 = (c == 1 or c == -1)
        elif R == sympy.QQ:
            h4 = (c != 0)
        elif getattr(R, 'is_Field', False):
            h4 = (c != R.zero)
        elif hasattr(R, 'is_unit'):
            h4 = bool(R.is_unit(c))
        else:
            h4 = (c == R.one or c == -R.one)
    except Exception:
        h4 = False

    # neg_Q: f is irreducible over R iff f is irreducible over F FAILS
    try:
        def is_irred(poly, dom):
            p = poly.set_domain(dom)
            if p.degree() <= 0:
                if dom == sympy.QQ or getattr(dom, 'is_Field', False):
                    return False
                if dom == sympy.ZZ:
                    try:
                        return sympy.isprime(abs(int(p.as_expr())))
                    except Exception:
                        return False
                return False
            else:
                cont, factors = p.factor_list()
                if dom == sympy.QQ or getattr(dom, 'is_Field', False):
                    is_u = (cont != dom.zero)
                elif dom == sympy.ZZ:
                    is_u = (cont == 1 or cont == -1)
                elif hasattr(dom, 'is_unit'):
                    is_u = dom.is_unit(cont)
                else:
                    is_u = (cont == dom.one or cont == -dom.one)
                return len(factors) == 1 and factors[0][1] == 1 and is_u

        irred_R = is_irred(f, R)
        irred_F = is_irred(f, F)
        neg_q = not (irred_R == irred_F)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: f is a polynomial over R",
    "H_4: f is primitive over R",
    "neg_Q: Equivalence of irreducibility over R and over F fails"
]

N_HYP = 4
NEG_Q_INDEX = 4