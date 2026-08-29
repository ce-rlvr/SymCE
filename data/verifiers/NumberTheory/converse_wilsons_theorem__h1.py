import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named bindings needed for NumberTheory

def conditions(witness) -> list[bool]:
    # H_1: n > 1
    try:
        h1 = bool(witness > 1)
    except Exception:
        h1 = False

    # H_2: (n-1)! \equiv -1 \pmod n
    try:
        fact = sympy.factorial(witness - 1)
        h2 = bool(sympy.Mod(fact, witness) == sympy.Mod(-1, witness))
        if not h2:
            try:
                h2 = bool((fact % witness) == ((-1) % witness))
            except Exception:
                pass
    except Exception:
        h2 = False

    # ¬Q: n is not a prime number
    try:
        neg_q = not sympy.isprime(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1",
    "H_2: (n-1)! \\equiv -1 \\pmod n",
    "¬Q: n is not a prime number"
]

N_HYP = 2
NEG_Q_INDEX = 2