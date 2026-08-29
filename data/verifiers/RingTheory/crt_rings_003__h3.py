import math
from functools import reduce
import sympy
from sympy import Integer

# Top-level setup
x, y, z = sympy.symbols('x y z')
Z = sympy.S.Integers

def conditions(witness) -> list[bool]:
    """
    Given a witness (a list of integers representing generators of ideals in Z),
    returns a list of booleans: [H_1, H_2, neg_Q].
    """
    try:
        # Allow witness to be a list of integers, or a tuple like ("Z", [2, 4])
        if isinstance(witness, tuple) and len(witness) == 2 and witness[0] in ("Z", Z, "Integers"):
            ideals = witness[1]
        else:
            ideals = witness
            
        # H_1: R is a ring with identity. 
        # We implicitly use R = Z, which is a ring with identity.
        # We just verify the witness is a valid list of integers.
        h1 = isinstance(ideals, (list, tuple)) and all(isinstance(val, (int, Integer)) for val in ideals)
    except Exception:
        h1 = False

    try:
        # H_2: I_1, I_2, ..., I_n are ideals of R.
        # In Z, any integer generates an ideal. We just need at least one ideal.
        h2 = h1 and len(ideals) >= 1
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            def lcm(a, b):
                a, b = int(a), int(b)
                if a == 0 and b == 0: 
                    return 0
                return abs(a * b) // math.gcd(a, b)
                
            lcm_val = reduce(lcm, ideals)
            
            def prod(a, b):
                return int(a) * int(b)
                
            prod_val = reduce(prod, ideals)
            
            if len(ideals) == 1:
                # R/I_1 is always isomorphic to R/I_1
                neg_q = False
            else:
                # The intersection of ideals <a_i> in Z is <lcm(a_i)>.
                # The quotient R / <lcm(a_i)> has size abs(lcm(a_i)) (or infinite if 0).
                # The product of quotients has size prod(abs(a_i)) (or infinite if any is 0).
                # For finitely generated abelian groups, if sizes differ, they are not isomorphic.
                if lcm_val == 0 and prod_val == 0:
                    zeros_count = sum(1 for val in ideals if int(val) == 0)
                    if zeros_count > 1:
                        # Z is not isomorphic to Z x Z x ...
                        neg_q = True
                    else:
                        non_zeros = [abs(int(val)) for val in ideals if int(val) != 0]
                        if any(val > 1 for val in non_zeros):
                            # Z is not isomorphic to Z x finite_group (where finite_group is non-trivial)
                            neg_q = True
                        else:
                            # Z is isomorphic to Z x {0}
                            neg_q = False
                else:
                    # If sizes are different, they are not isomorphic.
                    # If sizes are the same, they are isomorphic (since it implies pairwise coprime).
                    neg_q = abs(lcm_val) != abs(prod_val)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I_1, I_2, ..., I_n are ideals of R",
    "¬Q: R/(intersection of I_k) is not isomorphic to the product of R/I_k"
]

N_HYP = 2
NEG_Q_INDEX = 2