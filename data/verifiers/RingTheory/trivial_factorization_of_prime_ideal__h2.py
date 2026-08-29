import sympy
from sympy import symbols, Rational, Integer

# Top-level setup for witness expressions
Z = sympy.S.Integers
Q = sympy.S.Rationals
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (I, J, P) or (R, I, J, P) representing ideals.
    For principal ideals in Z or polynomial rings, they can be given as generators (e.g., integers or polynomials).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                I, J, P = witness
            elif len(witness) == 4:
                R, I, J, P = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            I = witness.get('I')
            J = witness.get('J')
            P = witness.get('P')
            if I is None or J is None or P is None:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def is_valid_ideal(a):
        try:
            if type(a).__name__ == 'Ideal':
                return True
            a_val = sympy.sympify(a)
            return isinstance(a_val, (sympy.Expr, int, float))
        except Exception:
            return False

    def same_ideal(a, b):
        try:
            if type(a).__name__ == 'Ideal' and type(b).__name__ == 'Ideal':
                return a == b
        except Exception:
            pass
        
        try:
            a_val = sympy.sympify(a)
            b_val = sympy.sympify(b)
            if a_val == 0 and b_val == 0:
                return True
            if a_val == 0 or b_val == 0:
                return False
            # In Z, principal ideals are equal iff generators are equal in absolute value
            if a_val.is_Integer and b_val.is_Integer:
                return abs(a_val) == abs(b_val)
            # In fields of fractions, they generate the same ideal if they differ by a constant unit
            ratio = sympy.simplify(a_val / b_val)
            return ratio.is_number and ratio != 0
        except Exception:
            return False

    try:
        # H1: R is a commutative ring
        # By using integers or polynomials, we implicitly work in a commutative ring (Z or Q[x,y,...])
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # H2: I and J are ideals of R
        h2_ok = is_valid_ideal(I) and is_valid_ideal(J)
    except Exception:
        h2_ok = False

    try:
        # H3: The product ideal IJ is equal to P
        h3_ok = same_ideal(I * J, P)
    except Exception:
        h3_ok = False

    try:
        # ¬Q: I != P and J != P
        neg_q_ok = not same_ideal(I, P) and not same_ideal(J, P)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: The product ideal IJ is equal to P",
    "¬Q: I != P and J != P"
]

N_HYP = 3
NEG_Q_INDEX = 3