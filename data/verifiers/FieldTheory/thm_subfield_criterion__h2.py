import sympy
from sympy.ntheory import isprime, factorint

# Top-level setup
# (No specific named bindings are required for this Field Theory conjecture, 
# as witnesses are expected to be tuples/dicts of parameters.)

def is_prime_power(k):
    try:
        k_int = int(k)
        if k_int != k or k_int < 2:
            return False
        return len(factorint(k_int)) == 1
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            p = witness.get('p')
            m = witness.get('m')
            n = witness.get('n')
        else:
            F, p, m, n = witness
            
        if hasattr(F, 'order'):
            F_order = int(F.order)
        elif hasattr(F, 'mod'):
            F_order = int(F.mod)
        else:
            F_order = int(F)
    except Exception:
        return [False, False, False, False]

    # H1: F is a finite field
    try:
        h1 = is_prime_power(F_order)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(int(p)) and int(p) == p)
    except Exception:
        h2 = False

    # H3: m is a positive integer
    try:
        h3 = bool(int(m) == m and int(m) > 0)
    except Exception:
        h3 = False

    # neg_Q: F contains a subfield of order p^m if and only if m divides n
    try:
        if int(n) != n:
            neg_q = False
        else:
            if not h1:
                has_subfield = False
            else:
                factors = factorint(F_order)
                p_F = list(factors.keys())[0]
                s = list(factors.values())[0]
                if p_F == int(p) and s % int(m) == 0:
                    has_subfield = True
                else:
                    has_subfield = False
            
            m_divides_n = (int(n) % int(m) == 0)
            
            conclusion = (has_subfield == m_divides_n)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "H_2: p is a prime number",
    "H_3: m is a positive integer",
    "¬Q: F contains a subfield of order p^m is NOT equivalent to m divides n"
]

N_HYP = 3
NEG_Q_INDEX = 3