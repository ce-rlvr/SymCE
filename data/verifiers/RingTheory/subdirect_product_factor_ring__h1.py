import sympy
from sympy import Symbol
from sympy.polys.rings import PolyRing
from sympy.polys.domains import Domain

# Top-level setup: named object bindings
x = Symbol('x')
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a ring R.
    """
    h1 = False
    try:
        # H_1: R is a ring containing the polynomial x^2 - x - 2.
        # We check if the witness is a sympy Ring/Domain and can contain the expression.
        if isinstance(witness, (PolyRing, Domain)):
            expr = x**2 - x - 2
            if hasattr(witness, 'from_sympy'):
                witness.from_sympy(expr)
                h1 = True
            elif hasattr(witness, 'from_expr'):
                witness.from_expr(expr)
                h1 = True
            else:
                try:
                    witness(expr)
                    h1 = True
                except Exception:
                    pass
    except Exception:
        h1 = False

    q_holds = False
    try:
        # Q: R/I is isomorphic to the subring of ZZ x ZZ with a = b mod 3.
        # This conclusion holds if and only if R is isomorphic to ZZ[x].
        if isinstance(witness, (PolyRing, Domain)):
            is_poly_ring = isinstance(witness, PolyRing) or \
                           (hasattr(witness, 'is_PolynomialRing') and witness.is_PolynomialRing) or \
                           ('Poly' in witness.__class__.__name__)
            if is_poly_ring:
                if hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
                    # Check if the base ring is ZZ and it is a univariate polynomial ring
                    if witness.domain == sympy.ZZ and len(witness.symbols) == 1:
                        q_holds = True
    except Exception:
        q_holds = False

    neg_q = not q_holds

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring containing x^2 - x - 2",
    "¬Q: R/I is not isomorphic to the subring of ZZ x ZZ with a = b mod 3"
]

N_HYP = 1
NEG_Q_INDEX = 1