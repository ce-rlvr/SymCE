import sympy as sp
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
O2 = zeros(2, 2)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, e, f) where R is a finite list of ring elements,
    and e, f are elements of R. The elements must support +, *, and ==.
    """
    try:
        R, e, f = witness
    except Exception:
        return [False, False, False, False]

    # Check if R is a valid ring
    try:
        z = None
        for cand in R:
            if all(cand + x == x for x in R) and all(x + cand == x for x in R):
                z = cand
                break
        
        u = None
        for cand in R:
            if all(cand * x == x for x in R) and all(x * cand == x for x in R):
                u = cand
                break
                
        is_valid_ring = (z is not None) and (u is not None)
        if is_valid_ring:
            for x in R:
                if not any(x + y == z for y in R):
                    is_valid_ring = False
                    break
                for y in R:
                    if (x + y) not in R:
                        is_valid_ring = False
                        break
                    if (x * y) not in R:
                        is_valid_ring = False
                        break
    except Exception:
        is_valid_ring = False

    # H1: e and f are idempotent elements in R
    try:
        h1 = is_valid_ring and (e in R) and (f in R) and (e * e == e) and (f * f == f)
    except Exception:
        h1 = False

    # H2: e and f are orthogonal, meaning ef = 0
    try:
        h2 = is_valid_ring and (e * f == z)
    except Exception:
        h2 = False

    # H3: e + f = 1
    try:
        h3 = is_valid_ring and (e + f == u)
    except Exception:
        h3 = False

    # Conclusion: Ann_R(e) + Ann_R(f) = R
    # Negated Conclusion: Ann_R(e) + Ann_R(f) != R
    # Ann_R(e) is the two-sided annihilator ideal of e: {a in R | aRe = 0 and eRa = 0}
    try:
        if not is_valid_ring:
            neg_q = False
        else:
            Ann_e = []
            for a in R:
                if all(a * x * e == z for x in R) and all(e * x * a == z for x in R):
                    Ann_e.append(a)
                    
            Ann_f = []
            for a in R:
                if all(a * x * f == z for x in R) and all(f * x * a == z for x in R):
                    Ann_f.append(a)
                    
            sum_ideals = []
            for a in Ann_e:
                for b in Ann_f:
                    s = a + b
                    if s not in sum_ideals:
                        sum_ideals.append(s)
                        
            q = True
            for x in R:
                if x not in sum_ideals:
                    q = False
                    break
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: e and f are idempotent elements in R",
    "H_2: e and f are orthogonal (ef = 0)",
    "H_3: e + f = 1",
    "¬Q: Ann_R(e) + Ann_R(f) != R"
]

N_HYP = 3
NEG_Q_INDEX = 3