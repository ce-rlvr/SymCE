import sympy
import math
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals
C = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the rings R1, R2 and the ideals I1, J1, I2, J2.
    In the standard representation, rings are given by their characteristic n (0 for Z),
    and ideals are given by a single generator.
    """
    try:
        if isinstance(witness, dict):
            R1 = witness.get("R1", witness.get("n1", 0))
            R2 = witness.get("R2", witness.get("n2", 0))
            I1 = witness.get("I1", witness.get("a1", 0))
            J1 = witness.get("J1", witness.get("b1", 0))
            I2 = witness.get("I2", witness.get("a2", 0))
            J2 = witness.get("J2", witness.get("b2", 0))
        elif hasattr(witness, "R1") and hasattr(witness, "I1"):
            R1 = getattr(witness, "R1", 0)
            R2 = getattr(witness, "R2", 0)
            I1 = getattr(witness, "I1", 0)
            J1 = getattr(witness, "J1", 0)
            I2 = getattr(witness, "I2", 0)
            J2 = getattr(witness, "J2", 0)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 6:
                R1, R2, I1, J1, I2, J2 = witness
            elif len(witness) == 2 and len(witness[0]) == 3 and len(witness[1]) == 3:
                R1, I1, J1 = witness[0]
                R2, I2, J2 = witness[1]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        def extract_gen(ideal):
            if isinstance(ideal, (tuple, list)) and len(ideal) == 1:
                return ideal[0]
            return ideal
            
        I1 = extract_gen(I1)
        J1 = extract_gen(J1)
        I2 = extract_gen(I2)
        J2 = extract_gen(J2)
        
        def get_char(ring):
            if ring == sympy.S.Integers:
                return 0
            try:
                return int(ring)
            except Exception:
                return 0
                
        n1 = get_char(R1)
        n2 = get_char(R2)
        
    except Exception:
        return [False, False, False]

    # H_1: R1 and R2 are rings
    # In our model, any integer n represents the ring Z/nZ (or Z if n=0), which is always a valid ring.
    h1_ok = True

    # H_2: I1 and J1 are ideals of R1 such that I1 + J1 = R1
    try:
        g1 = sympy.gcd(I1, J1)
        if n1 != 0:
            g1 = sympy.gcd(g1, n1)
            
        h2_ok = bool(g1 == 1 or g1 == -1)
    except Exception:
        h2_ok = False

    # ¬Q: The product ideals I1 x I2 and J1 x J2 are not comaximal in R1 x R2
    try:
        g2 = sympy.gcd(I2, J2)
        if n2 != 0:
            g2 = sympy.gcd(g2, n2)
            
        g2_is_unit = bool(g2 == 1 or g2 == -1)
        
        # The product ideals are comaximal in R1 x R2 iff they are comaximal in R1 AND in R2.
        # Thus, they are NOT comaximal (neg_Q is True) iff they fail to be comaximal in at least one component.
        neg_q_ok = not (h2_ok and g2_is_unit)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "H_2: I1 and J1 are ideals of R1 such that I1 + J1 = R1",
    "¬Q: The product ideals I1 x I2 and J1 x J2 are not comaximal in R1 x R2"
]

N_HYP = 2
NEG_Q_INDEX = 2