import sympy
import sympy.polys
from sympy import Symbol, totient

x = Symbol('x')

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and witness > 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            Phi_n = sympy.cyclotomic_poly(n, x)
            is_irred = sympy.polys.polytools.is_irreducible(Phi_n, domain='QQ')
            deg_correct = sympy.degree(Phi_n, x) == totient(n)
            is_isomorphic = is_irred and deg_correct
            neg_q = not is_isomorphic
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The factor ring is not isomorphic to the n-th cyclotomic field"
]

N_HYP = 1
NEG_Q_INDEX = 1