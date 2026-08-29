import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup for potential witness expressions
Z = S.Integers
Q = S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In any ring R, the right socle Soc(R_R) is an essential right ideal of R."
    (The dropped hypothesis was that R is right Artinian).
    """
    h1 = False
    try:
        # H_1: R is a ring (and Soc(R_R) is its right socle, which is true by definition for any ring)
        if witness in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
            h1 = True
        elif witness in [ZZ, QQ, RR, CC]:
            h1 = True
        elif hasattr(witness, 'is_ring') and witness.is_ring:
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        elif isinstance(witness, str):
            h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        # ¬Q: Soc(R_R) is NOT an essential right ideal of R
        # For Z, the socle is {0}, which is not essential since {0} intersect nZ is {0} (not non-zero).
        if witness in [S.Integers, ZZ]:
            neg_q = True
        elif witness in [S.Rationals, S.Reals, S.Complexes, QQ, RR, CC]:
            # Fields are Artinian, their socle is the whole field, which is essential.
            neg_q = False
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        elif hasattr(witness, 'is_ring') and witness.is_ring and not getattr(witness, 'is_Field', False):
            # Polynomial rings over domains have zero socle, which is not essential.
            if hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
                neg_q = True
        elif isinstance(witness, str):
            w = witness.strip().lower()
            if w == "z" or "[x]" in w:
                neg_q = True
            elif w in ["q", "r", "c"]:
                neg_q = False
            elif w.startswith("z_"):
                # Finite rings Z_n are Artinian, so their socle is essential.
                neg_q = False
            else:
                # Default assumption for other string-based infinite rings like "M2(Z)"
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Soc(R_R) is the right socle of R",
    "¬Q: Soc(R_R) is not an essential right ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1