import sympy
from sympy import ZZ, QQ, Symbol

# Top-level setup for potential witness expressions
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are ideals of R",
    "H_3: The quotient ring R/J is Artinian",
    "¬Q: The quotient ring R/(I \\cap J) is not Artinian"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple: (R, I_gens, J_gens)
    where R is the ring (e.g., ZZ or 'QQ[x]'), and I_gens, J_gens are lists of generators.
    For convenience, a 2-tuple (I_gens, J_gens) implicitly assumes R = ZZ.
    """
    try:
        if len(witness) == 3:
            R, I_gens, J_gens = witness
        elif len(witness) == 2:
            R = ZZ
            I_gens, J_gens = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a ring
    # We restrict to PIDs ZZ and QQ[x] where ideal arithmetic via gcd/lcm is straightforward.
    try:
        h1 = R in [ZZ, 'ZZ', 'Z', 'QQ[x]', 'Q[x]']
    except Exception:
        h1 = False

    # H_2: I and J are ideals of R
    try:
        if not (isinstance(I_gens, (list, tuple)) and isinstance(J_gens, (list, tuple))):
            h2 = False
        else:
            valid = True
            for gen in list(I_gens) + list(J_gens):
                if not isinstance(gen, (int, sympy.Integer, sympy.Expr)):
                    valid = False
            h2 = valid
    except Exception:
        h2 = False

    # H_3: The quotient ring R/J is Artinian
    # In ZZ or QQ[x], R/J is Artinian iff J is not the zero ideal.
    try:
        j_val = 0
        for gen in J_gens:
            j_val = sympy.gcd(j_val, gen)
        h3 = (j_val != 0)
    except Exception:
        h3 = False

    # ¬Q: The quotient ring R/(I \cap J) is not Artinian
    # In ZZ or QQ[x], R/(I \cap J) is not Artinian iff I \cap J is the zero ideal.
    try:
        i_val = 0
        for gen in I_gens:
            i_val = sympy.gcd(i_val, gen)
            
        j_val = 0
        for gen in J_gens:
            j_val = sympy.gcd(j_val, gen)
            
        if i_val == 0 or j_val == 0:
            cap_val = 0
        else:
            cap_val = sympy.lcm(i_val, j_val)
            
        neg_q = (cap_val == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]