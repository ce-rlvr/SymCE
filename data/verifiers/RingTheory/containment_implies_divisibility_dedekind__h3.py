import sympy
from sympy import ZZ, QQ, S
import math
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a Dedekind domain R, for any non-zero ideals I and J, there exists an ideal K such that I = JK."
    
    The true theorem requires I to be a subset of J (i.e. I \subseteq J).
    Without this, J does not necessarily divide I.
    
    Expected witness: (R, I, J) or (I, J) where R is a Dedekind domain (e.g., ZZ)
    and I, J are ideals represented by their generators.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            R, I, J = witness
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            R = ZZ
            I, J = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Normalize R to check if it's the ring of integers
    try:
        if R == ZZ or R == S.Integers or str(R) in ["Z", "ZZ", "Integers", "Z_ring"]:
            R_is_ZZ = True
        else:
            R_is_ZZ = False
    except Exception:
        R_is_ZZ = False

    # H_1: R is a Dedekind domain
    try:
        h1 = False
        if R_is_ZZ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif hasattr(R, 'is_Dedekind') and R.is_Dedekind:
            h1 = True
    except Exception:
        h1 = False

    # H_2: I and J are non-zero ideals of R
    try:
        h2 = False
        gen_I = None
        gen_J = None
        if R_is_ZZ:
            def get_gen(ideal):
                if isinstance(ideal, (int, sympy.Integer)):
                    return abs(int(ideal))
                elif isinstance(ideal, (list, tuple, set)):
                    lst = list(ideal)
                    if not lst:
                        return 0
                    g = int(lst[0])
                    for val in lst[1:]:
                        g = math.gcd(g, int(val))
                    return abs(g)
                return None
            
            gen_I = get_gen(I)
            gen_J = get_gen(J)
            
            if gen_I is not None and gen_J is not None:
                h2 = (gen_I != 0) and (gen_J != 0)
        else:
            # Fallback for other rings
            if I != 0 and J != 0:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist an ideal K of R such that I = JK
    try:
        neg_q = False
        if R_is_ZZ and h2:
            # In ZZ, I = JK means the generator of J divides the generator of I
            # So the conclusion fails if gen_J does NOT divide gen_I
            neg_q = (gen_I % gen_J != 0)
        elif not R_is_ZZ and h2:
            # Fallback for other rings: try to check divisibility
            try:
                rem = sympy.rem(I, J)
                neg_q = (rem != 0)
            except Exception:
                try:
                    rem = I % J
                    neg_q = (rem != 0)
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "H_2: I and J are non-zero ideals of R",
    "¬Q: There does not exist an ideal K of R such that I = JK"
]

N_HYP = 2
NEG_Q_INDEX = 2