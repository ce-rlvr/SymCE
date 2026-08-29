import sympy
from sympy import Symbol

# Top-level setup
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: F_p is the finite field of order p",
    "¬Q: The polynomial x^4 + 1 is irreducible over F_p"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if hasattr(witness, 'order'):
            p = int(witness.order)
        elif hasattr(witness, 'mod'):
            p = int(witness.mod)
        else:
            p = int(witness)
    except Exception:
        return [False, False]

    # H_1: F_p is the finite field of order p
    # This implies p must be a prime number.
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # ¬Q: The polynomial x^4 + 1 is irreducible over F_p
    try:
        if not h1:
            neg_q = False
        else:
            # Factor the polynomial modulo p
            factored = sympy.factor(x**4 + 1, modulus=p)
            # If it factors into smaller polynomials, it will be a Mul or Pow
            if isinstance(factored, (sympy.Mul, sympy.Pow)):
                neg_q = False
            else:
                # If it remains an Add (x**4 + 1), it is irreducible
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]