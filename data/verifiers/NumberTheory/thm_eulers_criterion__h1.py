import sympy

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: p does not divide a",
    "¬Q: a is a quadratic residue modulo p if and only if a^{(p-1)/2} \\equiv 1 \\pmod p fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_int(x):
    return isinstance(x, int) or isinstance(x, sympy.Integer)

def conditions(witness):
    try:
        # Witness should be a tuple (a, p)
        if len(witness) != 2:
            return [False, False, False]
        a, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_int(a))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_int(p) and p != 0 and (a % p != 0))
    except Exception:
        h2 = False
        
    try:
        if not is_int(a) or not is_int(p) or p == 0:
            neg_q = False
        else:
            p_abs = abs(p)
            is_qr = False
            for x in range(p_abs):
                if (x * x) % p_abs == a % p_abs:
                    is_qr = True
                    break
                    
            if p % 2 != 0:
                exp = (p - 1) // 2
                try:
                    rhs = (pow(int(a), int(exp), int(p_abs)) == 1)
                except ValueError:
                    # If pow fails (e.g., negative exponent and base not invertible),
                    # the expression is undefined, making the equivalence false.
                    rhs = False
            else:
                # If p is even, (p-1)/2 is not an integer, so the congruence is invalid/false.
                rhs = False
                
            q = (is_qr == rhs)
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]