import sympy
from sympy.ntheory import factorint, mobius
from sympy import divisors

# Top-level setup
GF = sympy.GF

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: There does not exist an irreducible polynomial of degree n with coefficients in F"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F_rep = witness.get('F', witness.get('q'))
            n = witness.get('n')
        else:
            F_rep, n = witness
    except Exception:
        return [False, False]
        
    try:
        if hasattr(F_rep, 'order'):
            q = int(F_rep.order)
        elif hasattr(F_rep, 'mod'):
            q = int(F_rep.mod)
        else:
            q = int(F_rep)
            
        if q < 2:
            h1_ok = False
        else:
            h1_ok = len(factorint(q)) == 1
    except Exception:
        h1_ok = False
        q = 2  # Fallback to prevent errors in neg_q evaluation

    try:
        n_val = int(n)
        if n_val != n:
            neg_q_ok = False
        elif n_val < 1:
            # There are no irreducible polynomials of degree <= 0
            neg_q_ok = True
        else:
            # Gauss's formula for the number of irreducible polynomials of degree n over GF(q)
            count = sum(mobius(n_val // d) * (q ** d) for d in divisors(n_val)) // n_val
            neg_q_ok = (count == 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]