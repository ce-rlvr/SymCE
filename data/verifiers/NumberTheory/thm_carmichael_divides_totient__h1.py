import sympy
from sympy.ntheory import totient, reduced_totient

# Top-level setup
# (No named bindings are required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        n = sympy.sympify(witness)
        if not n.is_integer:
            neg_q = False
        else:
            n_int = int(n)
            lam = reduced_totient(n_int)
            phi = totient(n_int)
            
            if lam == 0:
                neg_q = (phi != 0)
            else:
                neg_q = (phi % lam != 0)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: lambda(n) does not divide phi(n)"
]

N_HYP = 0
NEG_Q_INDEX = 0