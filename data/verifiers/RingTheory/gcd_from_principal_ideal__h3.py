import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion.
    
    Expected witness: (R, a, b, d)
    where R is a SymPy domain (e.g., ZZ, QQ), and a, b, d are elements of R.
    """
    if isinstance(witness, dict):
        R = witness.get('R')
        a = witness.get('a')
        b = witness.get('b')
        d = witness.get('d')
    else:
        try:
            R, a, b, d = witness
        except Exception:
            return [False, False, False]

    # H_1: R is an integral domain
    try:
        # In SymPy, Domain objects (like ZZ, QQ, ZZ[x]) represent integral domains.
        h1_ok = hasattr(R, 'is_Domain') and R.is_Domain
    except Exception:
        h1_ok = False

    # H_2: a and b are elements of R
    try:
        h2_ok = (a in R) and (b in R)
    except Exception:
        h2_ok = False

    # ¬Q: d is NOT a greatest common divisor of a and b in R
    try:
        if d not in R:
            is_gcd = False
        else:
            a_R = R.convert(a)
            b_R = R.convert(b)
            d_R = R.convert(d)
            
            # Compute a standard GCD in R
            g = R.gcd(a_R, b_R)
            
            def divides(domain, num, den):
                if den == domain.zero:
                    return num == domain.zero
                try:
                    q = domain.exquo(num, den)
                    return q is not None
                except Exception:
                    return False
            
            # d is a GCD iff d divides g and g divides d
            div1 = divides(R, g, d_R)  # d divides g
            div2 = divides(R, d_R, g)  # g divides d
            is_gcd = div1 and div2
            
        neg_q_ok = not is_gcd
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: a and b are elements of R",
    "¬Q: d is not a greatest common divisor of a and b in R"
]

N_HYP = 2
NEG_Q_INDEX = 2