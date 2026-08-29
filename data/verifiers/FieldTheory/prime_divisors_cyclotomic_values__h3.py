import sympy

# Top-level setup
# No specific named bindings required for this conjecture

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            p = witness.get('p')
        else:
            n, a, p = witness
    except Exception:
        return [False, False, False]

    def is_int(val):
        if isinstance(val, int):
            return True
        if hasattr(val, 'is_integer'):
            if callable(val.is_integer):
                return val.is_integer()
            else:
                return bool(val.is_integer)
        return False

    # H_1: n >= 1 is an integer
    try:
        h1 = is_int(n) and int(n) >= 1
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = is_int(a)
    except Exception:
        h2 = False

    # ¬Q: p does not divide n and p is not 1 mod n
    try:
        if not is_int(p) or not is_int(n):
            neg_q = False
        else:
            n_val = int(n)
            p_val = int(p)
            
            divides = False
            if p_val != 0:
                divides = (n_val % p_val == 0)
            elif n_val == 0:
                divides = True
                
            if n_val != 0:
                mod_1 = (p_val % n_val == 1 % n_val)
            else:
                mod_1 = (p_val == 1)
            
            neg_q = not (divides or mod_1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: a is an integer",
    "¬Q: p does not divide n and p is not 1 mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2