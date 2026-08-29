import sympy
import math
from sympy import abc

Z = sympy.S.Integers
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
x = abc.x

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I and J are ideals of R",
    r"¬Q: R/(I \cap J) is not isomorphic to R/I \times R/J"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                ring = Z
                I, J = witness
            elif len(witness) == 3:
                ring, I, J = witness
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            ring = witness.get("ring", Z)
            I = witness.get("I")
            J = witness.get("J")
        else:
            return [False, False, False]

        is_Z = False
        if ring in ("Z", Z, int, "ZZ"):
            is_Z = True
        elif hasattr(ring, "name") and ring.name in ("Z", "ZZ", "Integers"):
            is_Z = True
        elif str(ring) in ("Z", "ZZ", "Integers"):
            is_Z = True

        def extract_gen(ideal):
            if isinstance(ideal, (int, sympy.Integer)):
                return int(ideal)
            if isinstance(ideal, str):
                s = ideal.upper().replace("Z", "").replace("*", "").strip()
                if s == "":
                    return 1
                elif s == "-":
                    return -1
                try:
                    return int(s)
                except ValueError:
                    pass
            if hasattr(ideal, "base_set") and ideal.base_set == sympy.S.Integers:
                if hasattr(ideal, "lamda"):
                    try:
                        val = ideal.lamda(1)
                        if isinstance(val, (int, sympy.Integer)):
                            return int(val)
                    except Exception:
                        pass
            return None

        if is_Z:
            h1 = True
            gen_I = extract_gen(I)
            gen_J = extract_gen(J)
            if gen_I is not None and gen_J is not None:
                h2 = True
                neg_q = (math.gcd(gen_I, gen_J) != 1)
        else:
            try:
                if hasattr(ring, "is_Ring") and ring.is_Ring:
                    h1 = True
                    if I in ring and J in ring:
                        h2 = True
                        g = ring.gcd(I, J)
                        if hasattr(g, "degree"):
                            neg_q = (g.degree() > 0)
                        elif hasattr(g, "is_constant"):
                            neg_q = not g.is_constant()
                        else:
                            neg_q = (g not in [ring.one, -ring.one])
            except Exception:
                pass

    except Exception:
        pass

    return [h1, h2, neg_q]