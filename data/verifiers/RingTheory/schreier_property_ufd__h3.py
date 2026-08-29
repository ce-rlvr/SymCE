import sympy
from sympy import Integer
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, b, c), checks if it is a valid counterexample to the false conjecture.
    We restrict the verification to the Unique Factorization Domain of integers (Z).
    """
    # H_1: R is a Unique Factorization Domain
    try:
        a, b, c = witness
        # Verify that the elements belong to Z (which is a UFD)
        h1 = all(isinstance(val, (int, Integer)) and not isinstance(val, bool) for val in (a, b, c))
    except Exception:
        h1 = False

    # H_2: a, b, and c are non-zero elements in R
    try:
        a, b, c = witness
        h2 = h1 and (a != 0 and b != 0 and c != 0)
    except Exception:
        h2 = False

    # ¬Q: There do NOT exist a_1, a_2 in R such that a = a_1 * a_2, a_1 | b, and a_2 | c
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            a, b, c = witness
            a_val = int(a)
            b_val = int(b)
            c_val = int(c)
            
            # Find all divisors of b in Z
            divs_b = sympy.divisors(abs(b_val))
            divs_b = set(divs_b) | set([-d for d in divs_b])
            
            # Find all divisors of c in Z
            divs_c = sympy.divisors(abs(c_val))
            divs_c = set(divs_c) | set([-d for d in divs_c])
            
            # Check if there exists any pair (a1, a2) satisfying the condition
            exists = False
            for a1 in divs_b:
                for a2 in divs_c:
                    if a1 * a2 == a_val:
                        exists = True
                        break
                if exists:
                    break
            
            # The conclusion fails if no such pair exists
            neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain (verified for R=Z)",
    "H_2: a, b, and c are non-zero elements in R",
    "¬Q: There do not exist a_1, a_2 in R such that a = a_1 * a_2, a_1 | b, and a_2 | c"
]

N_HYP = 2
NEG_Q_INDEX = 2