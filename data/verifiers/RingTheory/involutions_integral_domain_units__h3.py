import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: u is a unit in R",
    "¬Q: u != 1 and u != -1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Witness can be a tuple (R, u) or just u (defaulting to QQ as the ring)
        if isinstance(witness, tuple) and len(witness) == 2:
            R_input, u = witness
        else:
            R_input = QQ
            u = witness
            
        # Map common SymPy sets to their corresponding Poly Domains
        if R_input == sympy.S.Integers:
            R = ZZ
        elif R_input == sympy.S.Rationals:
            R = QQ
        elif R_input == sympy.S.Reals:
            R = RR
        elif R_input == sympy.S.Complexes:
            R = CC
        else:
            R = R_input
            
    except Exception:
        return [False, False, False]

    # H_1: R is an integral domain
    h1 = False
    try:
        if R in (ZZ, QQ, RR, CC):
            h1 = True
        elif getattr(R, 'is_Field', False):
            h1 = True
        else:
            from sympy.polys.domains import Domain
            # In SymPy, Domain objects are integral domains.
            # We exclude QuotientRing as it may have zero divisors.
            if isinstance(R, Domain) and R.__class__.__name__ != 'QuotientRing':
                h1 = True
    except Exception:
        h1 = False

    # H_2: u is a unit in R
    h2 = False
    try:
        if h1:
            u_sym = sympy.sympify(u)
            u_R = R.from_sympy(u_sym)
            if u_R != R.zero:
                # Try revert (multiplicative inverse) first
                try:
                    if hasattr(R, 'revert'):
                        inv = R.revert(u_R)
                        if R.mul(inv, u_R) == R.one:
                            h2 = True
                except Exception:
                    pass
                
                # Try exact quotient if revert failed or didn't exist
                if not h2:
                    try:
                        if hasattr(R, 'exquo'):
                            inv = R.exquo(R.one, u_R)
                            if R.mul(inv, u_R) == R.one:
                                h2 = True
                    except Exception:
                        pass
                
                # Fallback for fields (all non-zero elements are units)
                if not h2 and getattr(R, 'is_Field', False):
                    h2 = True
    except Exception:
        h2 = False

    # ¬Q: u != 1 and u != -1
    neg_q = False
    try:
        u_sym = sympy.sympify(u)
        if u_sym != 1 and u_sym != -1:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]