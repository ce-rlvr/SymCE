import sympy
from sympy import Symbol, symbols, Rational, Integer
from sympy.polys.domains import ZZ, QQ

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False

    # 1. Extract R and J from witness
    try:
        R = None
        J = None
        if isinstance(witness, tuple) and len(witness) == 2:
            R, J = witness
        elif isinstance(witness, dict) and 'R' in witness and 'J' in witness:
            R = witness['R']
            J = witness['J']
        else:
            R = getattr(witness, 'R', witness)
            J = getattr(witness, 'J', None)

        # Evaluate H1: J(R) is the Jacobson radical of R
        expected_J = None
        if hasattr(R, 'jacobson_radical'):
            expected_J = R.jacobson_radical()
        elif hasattr(R, 'jacobson'):
            expected_J = R.jacobson()

        if expected_J is not None:
            if J is None:
                J = expected_J
                h1 = True
            else:
                h1 = (J == expected_J)
        else:
            if hasattr(witness, 'is_jacobson_radical'):
                h1 = bool(witness.is_jacobson_radical(R, J))
            elif hasattr(witness, 'check_jacobson_radical'):
                h1 = bool(witness.check_jacobson_radical())
            else:
                h1 = False
    except Exception:
        h1 = False

    # 2. Evaluate Conclusion: The Jacobson radical of the quotient ring R/J(R) is the zero ideal.
    try:
        Q = None
        if hasattr(R, 'quotient'):
            Q = R.quotient(J)
        elif hasattr(R, 'quotient_ring'):
            Q = R.quotient_ring(J)
        else:
            Q = R / J

        J_Q = None
        if hasattr(Q, 'jacobson_radical'):
            J_Q = Q.jacobson_radical()
        elif hasattr(Q, 'jacobson'):
            J_Q = Q.jacobson()

        if J_Q is not None:
            is_zero = False
            if hasattr(J_Q, 'is_zero_ideal'):
                is_zero = bool(J_Q.is_zero_ideal())
            elif hasattr(J_Q, 'is_zero'):
                if callable(J_Q.is_zero):
                    is_zero = bool(J_Q.is_zero())
                else:
                    is_zero = bool(J_Q.is_zero)
            elif hasattr(Q, 'zero_ideal'):
                is_zero = (J_Q == Q.zero_ideal())
            elif hasattr(Q, 'zero'):
                if isinstance(J_Q, list):
                    is_zero = (len(J_Q) == 0) or (len(J_Q) == 1 and J_Q[0] == Q.zero)
                else:
                    is_zero = (J_Q == Q.zero)
            else:
                if isinstance(J_Q, list):
                    is_zero = (len(J_Q) == 0) or (len(J_Q) == 1 and J_Q[0] == 0)
                else:
                    is_zero = (J_Q == 0)

            neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: J(R) is the Jacobson radical of R",
    "¬Q: The Jacobson radical of the quotient ring R/J(R) is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1