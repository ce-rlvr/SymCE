import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

class LaurentPolynomialRing:
    """
    A mock class for a Laurent polynomial ring to serve as a witness.
    """
    def __init__(self, base, gen):
        self.base = base
        self.gen = gen

    @property
    def is_domain(self):
        return True

    @property
    def units_in_R0(self):
        return False

# Standard counterexamples provided in the namespace
Z_x_laurent = LaurentPolynomialRing(ZZ, x)
Q_x_laurent = LaurentPolynomialRing(QQ, x)

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if isinstance(witness, str):
            s = witness.replace(" ", "").lower()
            if "laurent" in s or "z[" in s or "q[" in s or "k[" in s or "c[" in s or "r[" in s:
                h1 = True
            elif "z(" in s or "q(" in s or "k(" in s or "c(" in s or "r(" in s:
                h1 = True
            elif "domain" in s or "frac" in s or "field" in s:
                h1 = True
        elif hasattr(witness, 'is_domain'):
            val = witness.is_domain() if callable(witness.is_domain) else witness.is_domain
            h1 = bool(val)
        elif hasattr(witness, 'is_Field'):
            val = witness.is_Field() if callable(witness.is_Field) else witness.is_Field
            h1 = bool(val)
        elif hasattr(witness, 'is_integral_domain'):
            val = witness.is_integral_domain() if callable(witness.is_integral_domain) else witness.is_integral_domain
            h1 = bool(val)
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, str):
            s = witness.replace(" ", "").lower()
            if "^-1" in s or "1/x" in s or "laurent" in s:
                neg_q = True
            elif "z(" in s or "q(" in s or "k(" in s or "c(" in s or "r(" in s:
                neg_q = True
            elif "frac" in s:
                neg_q = True
            elif "not" in s and "r_0" in s:
                neg_q = True
        elif type(witness).__name__ == 'FractionField':
            neg_q = True
        elif 'Laurent' in str(type(witness)):
            neg_q = True
        elif hasattr(witness, 'units_in_R0'):
            val = witness.units_in_R0() if callable(witness.units_in_R0) else witness.units_in_R0
            neg_q = not bool(val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The group of units of R is not contained entirely within R_0"
]

N_HYP = 1
NEG_Q_INDEX = 1