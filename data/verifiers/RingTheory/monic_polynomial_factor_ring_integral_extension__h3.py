import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy import Rational, Integer

# Standard algebra objects
Z2 = sympy.polys.domains.FF(2)
Z3 = sympy.polys.domains.FF(3)
Z5 = sympy.polys.domains.FF(5)
ZZ = sympy.polys.domains.ZZ
QQ = sympy.polys.domains.QQ

def conditions(witness) -> list[bool]:
    res = [False, False, False, False]
    
    try:
        if isinstance(witness, tuple):
            witness = witness[-1]
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
    except Exception:
        return res
        
    # H_1: R is a commutative ring with identity
    try:
        domain = f.domain
        # SymPy domains are commutative rings with identity
        if hasattr(domain, 'one') and hasattr(domain, 'zero'):
            res[0] = True
    except Exception:
        pass

    # H_2: f is a polynomial over R
    try:
        if len(f.gens) == 1:
            res[1] = True
    except Exception:
        pass

    # H_3: The degree of f is at least 1
    try:
        if f.degree() >= 1:
            res[2] = True
    except Exception:
        pass

    # not Q: R does not embed into the quotient ring or the quotient ring is not an integral extension of R
    try:
        domain = f.domain
        lc = f.LC()
        
        is_unit = False
        try:
            # Check if the leading coefficient is a unit in the domain
            domain.exquo(domain.one, lc)
            is_unit = True
        except Exception:
            is_unit = False
            
        # For integral domains, the natural map embeds R into the quotient ring (since deg >= 1),
        # and the quotient is an integral extension if and only if the leading coefficient is a unit.
        # Thus, the conclusion fails if and only if the leading coefficient is not a unit.
        res[3] = not is_unit
    except Exception:
        pass

    return res

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial over R",
    "H_3: The degree of f is at least 1",
    "not Q: R does not embed into the quotient ring or the quotient ring is not an integral extension of R"
]

N_HYP = 3
NEG_Q_INDEX = 3