import sympy
from sympy import sympify
from sympy.abc import x, y, z, t, u, v

def conditions(witness):
    try:
        if isinstance(witness, dict):
            I = witness.get("I")
            J = witness.get("J")
            P = witness.get("P")
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                _, I, J, P = witness
            elif len(witness) == 3:
                I, J, P = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
            
        if I is None or J is None or P is None:
            return [False] * 5
    except Exception:
        return [False] * 5

    # Try to treat the generators as integers (representing ideals in Z)
    try:
        I_val = int(I)
        J_val = int(J)
        P_val = int(P)
        # Verify they are actually integers or string representations of integers
        if (str(I_val) == str(I) or I_val == I) and \
           (str(J_val) == str(J) or J_val == J) and \
           (str(P_val) == str(P) or P_val == P):
            is_int_witness = True
        else:
            is_int_witness = False
    except Exception:
        is_int_witness = False

    if is_int_witness:
        h1 = True  # Z is a commutative ring
        h2 = True  # Any integer generates an ideal in Z
        h3 = True  # Any integer generates an ideal in Z
        try:
            if P_val == 0:
                h4 = (I_val * J_val == 0)
                i_sub = (I_val == 0)
                j_sub = (J_val == 0)
            else:
                h4 = (I_val * J_val) % P_val == 0
                i_sub = (I_val % P_val == 0)
                j_sub = (J_val % P_val == 0)
            neg_q = not (i_sub or j_sub)
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # Try to treat the generators as sympy expressions (representing ideals in Q[x, y, ...])
    try:
        I_expr = sympify(I)
        J_expr = sympify(J)
        P_expr = sympify(P)
        
        h1 = True  # Q[x, y, ...] is a commutative ring
        h2 = True  # Any polynomial generates an ideal
        h3 = True  # Any polynomial generates an ideal
        
        def divides(a, b):
            if b == 0:
                return a == 0
            num, den = sympy.fraction(sympy.cancel(a / b))
            return den.is_constant()

        h4 = bool(divides(I_expr * J_expr, P_expr))
        i_sub = bool(divides(I_expr, P_expr))
        j_sub = bool(divides(J_expr, P_expr))
        
        neg_q = not (i_sub or j_sub)
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    return [False] * 5

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "H_4: The product ideal IJ is a subset of P",
    "¬Q: Neither I nor J is a subset of P"
]

N_HYP = 4
NEG_Q_INDEX = 4