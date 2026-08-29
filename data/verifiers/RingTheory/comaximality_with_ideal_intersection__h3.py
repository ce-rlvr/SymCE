import sympy
from sympy import gcd, lcm, sympify

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        # Parse witness: expect either a dict or a tuple/list of 3 or 4 elements
        if isinstance(witness, dict):
            I_val = witness.get('I', witness.get('i'))
            J_val = witness.get('J', witness.get('j'))
            K_val = witness.get('K', witness.get('k'))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                I_val, J_val, K_val = witness
            elif len(witness) == 4:
                _, I_val, J_val, K_val = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def extract_gen(val):
        # If the ideal is given as a set or list with a single generator, extract it
        if isinstance(val, (set, list, tuple)) and len(val) == 1:
            return list(val)[0]
        return val

    try:
        I = sympify(extract_gen(I_val))
        J = sympify(extract_gen(J_val))
        K = sympify(extract_gen(K_val))
        
        # H1: R is a commutative ring and I, J, K are ideals.
        # We verify this by checking if we can compute GCD and LCM (valid for Z or F[x])
        gcd(I, J)
        lcm(J, K)
        h1 = True
    except Exception:
        h1 = False

    try:
        # H2: I and K are comaximal, meaning I + K = R.
        # For principal ideals, this means gcd(I, K) is a unit (1).
        h2 = (gcd(I, K) == 1)
    except Exception:
        h2 = False

    try:
        # ¬Q: I is NOT comaximal with J \cap K.
        # J \cap K corresponds to lcm(J, K).
        neg_q = (gcd(I, lcm(J, K)) != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring and I, J, K are ideals",
    "H_2: I and K are comaximal (I + K = R)",
    "¬Q: I is not comaximal with J \\cap K"
]

N_HYP = 2
NEG_Q_INDEX = 2