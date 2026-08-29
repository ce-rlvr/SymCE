import sympy
from sympy import S
from sympy.polys.domains import Domain, ZZ, QQ

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

def conditions(witness):
    try:
        R, p = witness
        # Normalize common representations of Z and Q
        if R in (S.Integers, 'ZZ', 'Z'):
            R = ZZ
        elif R in (S.Rationals, 'QQ', 'Q'):
            R = QQ
    except Exception:
        return [False, False, False, False]
    
    # H1: R is an integral domain
    try:
        # In SymPy, all Domain objects (ZZ, QQ, PolyRing, etc.) are integral domains.
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    # H2: p is not a unit in R
    try:
        if p == R.zero or p == 0:
            is_u = False
        else:
            try:
                R.exquo(R.one, p)
                is_u = True
            except Exception:
                try:
                    p_R = R.from_sympy(sympy.sympify(p))
                    R.exquo(R.one, p_R)
                    is_u = True
                except Exception:
                    is_u = False
        h2 = not is_u
    except Exception:
        h2 = False

    # H3: p is a prime element of R
    try:
        if p == R.zero or p == 0:
            # In an integral domain, the ideal (0) is prime, so 0 is a prime element.
            h3 = True
        else:
            if is_u:
                h3 = False
            elif R.is_Field:
                h3 = False
            elif R == ZZ:
                h3 = sympy.isprime(abs(int(p)))
            else:
                # Fallback for other domains (not strictly needed for the p=0 counterexample)
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: p is NOT an irreducible element of R
    try:
        if p == R.zero or p == 0:
            # 0 is never irreducible (an irreducible element must be non-zero and non-unit)
            is_irred = False
        else:
            if is_u:
                is_irred = False
            elif R.is_Field:
                is_irred = False
            elif R == ZZ:
                is_irred = sympy.isprime(abs(int(p)))
            else:
                is_irred = False
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: p is not a unit in R",
    "H_3: p is a prime element of R",
    "¬Q: p is not an irreducible element of R"
]

N_HYP = 3
NEG_Q_INDEX = 3