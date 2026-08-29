import math
import sympy
from sympy import ZZ, QQ, S
from sympy.abc import x, y, z

# Top-level setup for named object bindings
Z = ZZ
Q = QQ

def get_generator(I, R):
    """Helper to extract a principal generator for an ideal given as a list of elements."""
    if isinstance(I, (list, tuple, set)):
        if R in (ZZ, 'Z', 'ZZ', S.Integers):
            g = 0
            for elem in I:
                g = math.gcd(g, int(elem))
            return g
        elif R in (QQ, 'Q', 'QQ', S.Rationals, S.Reals, S.Complexes):
            for elem in I:
                if float(elem) != 0:
                    return 1
            return 0
        else:
            g = R.zero
            for elem in I:
                g = R.gcd(g, R(elem))
            return g
    else:
        return I

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    try:
        # Parse witness
        is_R_ideals = False
        if isinstance(witness, (list, tuple)) and len(witness) == 2:
            R_cand = witness[0]
            if R_cand in (ZZ, QQ, 'Z', 'ZZ', 'Q', 'QQ', S.Integers, S.Rationals, S.Reals, S.Complexes):
                is_R_ideals = True
            elif hasattr(R_cand, 'one') and hasattr(R_cand, 'zero'):
                is_R_ideals = True
                
        if is_R_ideals:
            R, ideals = witness
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            R = ZZ
            ideals = witness
        else:
            R, ideals = witness

        # H_1: R is a ring with identity
        try:
            if R in (ZZ, QQ, 'Z', 'ZZ', 'Q', 'QQ', S.Integers, S.Rationals, S.Reals, S.Complexes):
                h1 = True
            elif hasattr(R, 'one') and hasattr(R, 'zero'):
                h1 = True
        except Exception:
            pass

        # H_2: I_1, ..., I_n are ideals of R
        try:
            if isinstance(ideals, (list, tuple)) and len(ideals) >= 2:
                h2 = True
                for I in ideals:
                    gen = get_generator(I, R)
                    if R in (ZZ, 'Z', 'ZZ', S.Integers):
                        if not (isinstance(gen, int) or (hasattr(gen, 'is_Integer') and gen.is_Integer)):
                            h2 = False
                    elif R in (QQ, 'Q', 'QQ', S.Rationals, S.Reals, S.Complexes):
                        if not isinstance(gen, (int, float)) and not hasattr(gen, 'is_Rational'):
                            h2 = False
                    else:
                        R(gen) # Try to cast to ring element
            else:
                h2 = False
        except Exception:
            h2 = False

        # ¬Q: The ideals I_1, ..., I_n are NOT pairwise comaximal
        try:
            if h1 and h2:
                comaximal = True
                for i in range(len(ideals)):
                    for j in range(i + 1, len(ideals)):
                        gen_i = get_generator(ideals[i], R)
                        gen_j = get_generator(ideals[j], R)
                        
                        if R in (ZZ, 'Z', 'ZZ', S.Integers):
                            if math.gcd(int(gen_i), int(gen_j)) != 1:
                                comaximal = False
                        elif R in (QQ, 'Q', 'QQ', S.Rationals, S.Reals, S.Complexes):
                            if float(gen_i) == 0 and float(gen_j) == 0:
                                comaximal = False
                        else:
                            g = R.gcd(R(gen_i), R(gen_j))
                            if not R.is_unit(g):
                                comaximal = False
                neg_q = not comaximal
        except Exception:
            pass

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I_1, ..., I_n are ideals of R",
    "¬Q: The ideals I_1, ..., I_n are not pairwise comaximal"
]

N_HYP = 2
NEG_Q_INDEX = 2