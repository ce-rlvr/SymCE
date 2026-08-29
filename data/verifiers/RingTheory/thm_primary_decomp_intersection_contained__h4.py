import sympy
import math

# Top-level setup
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (q, i, j) or (R, q, i, j) representing
    the generators of the ideals Q, I, J in the ring of integers Z.
    """
    try:
        if isinstance(witness, dict):
            q = int(witness.get('Q', witness.get('q')))
            i = int(witness.get('I', witness.get('i')))
            j = int(witness.get('J', witness.get('j')))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                q, i, j = witness
            elif len(witness) == 4:
                _, q, i, j = witness
            else:
                return [False, False, False, False]
            q, i, j = int(q), int(i), int(j)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    # We are working in Z, which is a commutative ring.
    h1 = True

    # H_2: Q is a primary ideal of R
    try:
        abs_q = abs(q)
        if abs_q == 1:
            h2 = False
        elif abs_q == 0:
            h2 = True
        else:
            factors = sympy.factorint(abs_q)
            h2 = (len(factors) == 1)
    except Exception:
        h2 = False

    # H_3: I \cap J \subseteq Q
    try:
        lcm_ij = sympy.lcm(abs(i), abs(j))
        if q == 0:
            h3 = (lcm_ij == 0)
        else:
            h3 = (lcm_ij % abs(q) == 0)
    except Exception:
        h3 = False

    # ¬Q: J \not\subseteq \sqrt{Q}
    try:
        abs_q = abs(q)
        if abs_q == 0:
            rad_q = 0
        elif abs_q == 1:
            rad_q = 1
        else:
            factors = sympy.factorint(abs_q)
            rad_q = 1
            for p in factors:
                rad_q *= p
        
        if rad_q == 0:
            j_in_rad = (j == 0)
        else:
            j_in_rad = (j % rad_q == 0)
        
        neg_q = not j_in_rad
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q is a primary ideal of R",
    "H_3: I and J are ideals of R such that I \\cap J \\subseteq Q",
    "¬Q: J is not a subset of the radical of Q"
]

N_HYP = 3
NEG_Q_INDEX = 3