import sympy
from sympy import S
from sympy.polys.domains import CC, RR, QQ, ZZ, FF

# Top-level setup: named object bindings that the witness expression may reference.
Complexes = S.Complexes
Reals = S.Reals
Rationals = S.Rationals
Integers = S.Integers

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple (F, n) where F is a field and n is an integer.
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        F, n = witness
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist an irreducible polynomial of degree n with coefficients in F
    try:
        if n == 1:
            # Degree 1 polynomials are always irreducible in any field
            exists = True
        else:
            F_str = str(F)
            # In the field of complex numbers (or any algebraically closed field), 
            # there are no irreducible polynomials of degree > 1.
            if F == CC or F == Complexes or F_str in ['CC', 'C', 'Complexes', 'ComplexField']:
                exists = False
            # In the field of real numbers, irreducible polynomials can only have degree 1 or 2.
            elif F == RR or F == Reals or F_str in ['RR', 'R', 'Reals', 'RealField']:
                exists = (n == 2)
            else:
                # For QQ, finite fields, and most other standard fields, 
                # irreducible polynomials of any degree >= 1 exist.
                exists = True
        
        neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: There does not exist an irreducible polynomial of degree n with coefficients in F"
]

N_HYP = 1
NEG_Q_INDEX = 1